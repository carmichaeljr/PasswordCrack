# PasswordCrack
The solution to a challenge to crack a password

<p>
  This program was written in response to a challenge that my high school CS teacher gave me. The challenge is as follows:
</p>
<p>
    Given a zip file that is password protected, find the password and unzip the file. We were given two rules:
  
      . The password is 8 characters in length
      . The first 5 characters of the password are 'Super'
</p>
<p>  
  To run this program, make sure you have python 3 or greater installed. This program needs to be run from the command line and will not print out properly if run from the python IDLE.
  When the script asks you for the password length, <b>type in 3</b>, because thats how many characters are left after subtracting the first five characters of 'Super'. When finished the program should printout the final password, and will have unziped the file. 
  
  (Im not going to tell you the password because that would ruin the fun)
</p>
  
<h4>Design</h4>
<p>
  This project uses generator decorators to create the 'lists' of password combinations. Instead of creating an actual list, which would use up far to much memory, the generator just returns the next combination in the sequence. This dramaticly cuts down on memory use, with a small cost of increased logic.
