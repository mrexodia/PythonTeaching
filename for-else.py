# Make sure to import the course module to get helpful error messages
import course

for i in range(10):
    print(i)

    raise Exception("Something went wrong")
    if i == 9:
        print("Too big - I'm giving up!")
        break
else: # error
    print("Completed successfully")