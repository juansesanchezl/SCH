# write a program to generate the random string in upper and lower case letters.  
import random  
import string  

def random_lower_string(length):
    result = ''.join((random.choice(string.ascii_lowercase) for x in range(length)))
    return result

def Upper_Lower_string(length): # define the function and pass the length as argument  
    # Print the string in Lowercase  
    result = ''.join((random.choice(string.ascii_lowercase) for x in range(length))) # run loop until the define length  
    print(" Random string generated in Lowercase: ", result) 
  
    # Print the string in Uppercase  
    result1 = ''.join((random.choice(string.ascii_uppercase) for x in range(length))) # run the loop until the define length  
    print(" Random string generated in Uppercase: ", result1)  

def getNewPath(path):
    filetype = path.split(".")[-1]
    fullname = path.split("/")[-1]
    new_name = random_lower_string(8) + '.mp4'
    new_path = path.replace(fullname, new_name)
    return new_path



  
#Upper_Lower_string(8) # define the length  
#a_string = "docs.python.mp4"
#partitioned_string = a_string.split(".")[-1]
#print(partitioned_string)
path = r'videos/Video4-encoded.m4v'
#rslt = path.split('/')[-1]
#print(rslt)
new_p = getNewPath(path)
print(new_p)
