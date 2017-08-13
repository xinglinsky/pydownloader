# Movie Download Manager--Using it with pyspider
![docker](http://oukrrnfuf.bkt.clouddn.com/docker-small.png)

## OverView
### Some issue 
1. If you want download some movie in **China**, you always need **Windows** and **Thunder**.I run it with *Window10* and *Thunder 9*. 

***

## Setup
1. run mysql docker container.
2. run pyspider containers.
3. enter mysql container, login with username and password.  
   * execute command:  
   `docker exec -it mysql /bin/bash`  
   * like using *root* account:   
   `mysql -u root -p`
4. create database and table.  
   * database:   
   `create database downloaddb;`  
   * copy the content in *app.sql* and execute it:
***
    
## Link
PySpider: [http://docs.pyspider.org/en/latest/](http://docs.pyspider.org/en/latest/)