//https://medium.com/ameykpatil/how-to-publish-an-external-video-to-twitter-node-js-version-89c03b5ff4fe
const _ = require('lodash')
const request = require('request')
const Promise = require('bluebird')
const requestPost= Promise.promisify(request.post,{multiArgs: true})
const requestGet = Promise.promisify(request.get, {multiArgs: true})

const oAuthCredentials = {
    'consumer_key': 'FlEpsmTdOuKKTX5mHadyoTqFG',
    'consumer_secret': 'VBAz1TIDlR5r9MRnuBlIyO4t4erQQvD2C4P878xodrOW5QjJBE',
    'token': '1305341332102230018-vajWvAqmwidwwwYXxdAeqkrrHwWaem',
    'token_secret': 'QletoP2hX3skWMwzgtTnLgzfUZdKDBsycxUOAhRAljTX9'
  }

  const videoObj = {
    originalUrl: './videos/video2.mp4',
    videoMeta: {
      height: 123,
      width: 234,
      size: 1685018,
      duration: 120,
      mimeType: 'video/mp4'
    }
  }  

  const _initMediaUpload = function* (oAuthCredentials, videoObj) {
    const options = {
      url: 'https://upload.twitter.com/1.1/media/upload.json',
      oauth: oAuthCredentials,
      formData: {
        command: 'INIT',
        'media_type': videoObj.videoMeta.mimeType,
        'media_category': 'tweet_video',
        'total_bytes': videoObj.videoMeta.size
      }
    }
    try {
      const resultArray = yield requestPost(options)
      const resp = resultArray[0]
      const body = resultArray[1]
      const mediaId = JSON.parse(body).media_id_string
      return mediaId
    } catch (err) {
      throw err
    }
  }

  const _appendMediaUpload = function* (oAuthCredentials, data, mediaId, segmentIndex) {
    const options = {
      url: 'https://upload.twitter.com/1.1/media/upload.json',
      oauth: oAuthCredentials,
      form: {
        command: 'APPEND',
        'media_id': mediaId,
        'segment_index': segmentIndex,
        //media: data
        'media_data': data.toString('base64')
      }
    }
    try {
      const resultArray = yield requestPost(options)
      return
    } catch (err) {
      throw err
    }
  }

  const _finalizeMediaUpload = function* (oAuthCredentials, mediaId) {
    const options = {
      url: 'https://upload.twitter.com/1.1/media/upload.json',
      oauth: oAuthCredentials,
      formData: {
        command: 'FINALIZE',
        'media_id': mediaId
      }
    }
    try {
      const resultArray = yield requestPost(options)
      return
    } catch (err) {
      throw err
    }
  }

  const _getStatusMediaUpload = function* (oAuthCredentials, mediaId, lastProgressPercent) {
    const options = {
      url: 'https://upload.twitter.com/1.1/media/upload.json',
      oauth: oAuthCredentials,
      qs: {
        command: 'STATUS',
        'media_id': mediaId
      }
    }
    try {
      const resultArray = yield requestGet(options)
      const body = JSON.parse(resultArray[1])
      if (body['processing_info']) {
        // if processing info is present return it
        const processingInfo = body['processing_info']
        return processingInfo
      } else if (body.errors) {
        // if body contains errors build message & throw error 
        const message = _.get(body, 'errors.0.message')
        const code = _.get(body, 'errors.0.code')
        throw new Error(`${code} ${message}`)
      } else {
        // else return custom processing info
        const processingInfo = {
          state: 'unknown',
          'progress_percent': lastProgressPercent
        }
        return processingInfo
      }
    } catch (err) {
      throw err
    }
  }

  const _streamMediaToTwitter = function (oAuthCreds, videoObj, mediaId, cb) {
    let segmentIndex = 0
    let chunkUploadInProgress = false
    let streamReadingEnded = false 
    // if the video url is of S3  
    const filePath = videoObj.originalUrl
    const indexOfForwardSlash = filePath.lastIndexOf('/')
    const fileName = (indexOfForwardSlash !== -1) ? filePath.substr(indexOfForwardSlash + 1) : filePath
    const startIndex = 'https://'.length
    const endIndex = filePath.indexOf('.s3.amazonaws.com')
    const bucket = filePath.slice(startIndex, endIndex)
    const params = {
      Bucket: bucket,
      Key: fileName
    }
    //const res = s3.getObject(params).createReadStream()
    // if the video url is an external url
    const res = request.get(videoObj.originalUrl)
    res.on('response', function (resp) {
      if (resp.statusCode !== 200) {
        const error = new Error(`request failed : ${resp.statusCode}`)
        res.resume()
        return cb(error)
      }
    })
    res.on('error', function (err) {
      return cb(err)
    })
    res.on('data', function (chunk) {
      res.pause()
      chunkUploadInProgress = true
      Promise.coroutine(_appendMediaUpload)(oAuthCreds, chunk, mediaId, segmentIndex)
        .then(() => {
          segmentIndex++
          res.resume()
          chunkUploadInProgress = false
          Promise.resolve()
        })
        .then(() => {
          if (!chunkUploadInProgress && streamReadingEnded) {
            Promise.coroutine(_finalizeMediaUpload)(oAuthCreds, mediaId)
              .then(() => {
                return cb(null, mediaId)
              })
          }
        })
        .catch((err) => cb(err))
    })
    res.on('end', function () {
      streamReadingEnded = true
      if (!chunkUploadInProgress && streamReadingEnded) {
        Promise.coroutine(_finalizeMediaUpload)(oAuthCreds, mediaId)
          .then(() => {
            return cb(null, mediaId)
          })
      }
    })
  }

// initialize media upload & get mediaId
const mediaId = _initMediaUpload(oAuthCredentials, videoObj)
console.log(mediaId);
// stream from the video url to twitter
 Promise.promisify(_streamMediaToTwitter)(oAuthCredentials, videoObj, mediaId)
// check status & wait till the media upload is finished
let state = 'pending'
let progressPercent = 0 // you can print this to check progress
const startTime = Date.now()
do {
  const processingInfo =  _getStatusMediaUpload (oAuthCredentials, mediaId, progressPercent)
  state = processingInfo.state
  progressPercent = processingInfo.progress_percent
} while (state !== 'succeeded' && (Date.now() - startTime) < 30*1000)