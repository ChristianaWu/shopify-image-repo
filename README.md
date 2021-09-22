# Shopify Image Repository
This is a image repository with the capacity to sell/buy things. 
This was implemented using Flask. This is for the Data Engineering role, so I did not invest much time into the UI. Although with more time I could have. 

#Usage
To use this application, clone the repository, then enter the directory and then in the command line run "python run.py". This will create the appropriate database tables and start the Flask server. Once this is running open the web browser at the address given by Flaks, this is usually http://127.0.0.1:5000. 

Once you open the application you will see a table with all the images that could be bought. This will include the price, stock, the image, and the discounted price. In this table you can "buy" these images. Once you click on the link you will have to input information for shipping. address, etc. 

As a seller you can login you your account, the credentials are email: admin@gmail.com password: admin. From there you will be redirected to the home page. On the home page you will see a link to see you own account. There you will see all the images you have for sale and orders you have to full fill. You can edit the information about your images and add discounts. 

If you are a potential seller you can signup by going to the home page and signing up a new seller account.

#Futrue Development
If I were to continue with this project and add more features, I would add a way for sellers to upload their images. 
I would also add more test cases to improve my application to make sure there would be no bugs, but as time permitted, I wanted to demonstrate my knowledge of unit testing.  
