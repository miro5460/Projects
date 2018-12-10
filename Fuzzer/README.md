# Lab 9: The Fuzzer
# 7/25/18

# Michael Robinson


1. This tool is a way to determine if a website, in this case http://www.cs.tufts.edu/comp/20/hackme.php is vulnerable to XSS attacks.
2. This tool works by posting a specified payload to given/previously inspected/known sections of the page. In this case, I inspected the source code of the target site for <input> tags, since these would indicate potential vulnerabilities for XSS. This could become more powerful if it was automated in the program and didn't rely on the user to inspect the input fields and their associated names. Once, this was complete, and the input regions were specified ("fullname" and "beverage" in this case) any value could be given to fullname and as long as one of the four specified bebeverages was chosen, the form would be submitted through a post request. Inspecting the request content showed that this had successfully executed with the page's encoded response. It should be noted that even though the input field on the page specified that a maximum of 15 characters could be input, submitting through the fuzzer circumvented this.  
3. All basic aspects of this lab have been correctly implemented. I am currently working on adding functionality to work with Daniel Miessler's fuzzing lists.
4. I have discussed submitting webform information with Jay Facultad.
5. It took me approx 3hrs to complete this lab. (because I was being stupid and not looking at the source code of the website, led to some interesting reading though so not all bad!)


Sources:

Used this as a guide on how to correctly submit info
to a webform using requests module
1. https://dzone.com/articles/how-submit-webform-python
