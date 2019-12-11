aws_mysql_connect :
	mysql -h twitter-unifier-mysql.ceztlphuh76l.us-west-1.rds.amazonaws.com -P 3306 -u knownastron -p

deploy_react_app:
	sudo serve --ssl-cert /etc/letsencrypt/live/www.knownastron.com/fullchain.pem --ssl-key /etc/letsencrypt/live/www.knownastron.com/privkey.pem -s ./reactapp/build -l 5000
