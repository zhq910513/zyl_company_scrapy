db.createUser({user: 'readWrite', pwd: 'readWrite123456', roles: [{role: 'readWrite', db: 'zyl_company_scrapy'}]})



mongorestore -h 27.150.182.135:27017 --authenticationDatabase admin -u readWrite -p readWrite123456 -d zyl_company_scrapy --dir D:/zyl_company_scrapy