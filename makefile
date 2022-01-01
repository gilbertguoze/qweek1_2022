
msg ?= git add

.PHONY: tip git zsh clash
hello : 
	@echo "hello world"
	echo "second"
tip : 
	touch 78.md
	@echo 345 > 78.md
# 环境控制，目录名称，环境变量，文件复制

git : 
	-git pull origin master
	git add .
	-git commit -m "$(msg)"
	@echo $$?
#	if [$$? != 0]; \
#	then \
#		exit 1;\
#	fi;
	-git push -u origin master
zsh :
	git clone http://github.com/robbyrussell/oh-my-zsh.git ~/.oh-my-zsh
	cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc
#	sudo zsh | chsh -s /bin/zsh
	sudo chsh -s /bin/zsh


clash :
	-pkill -f clash-linux-amd64-v1.7.1
	sleep 10
	nohup ../clash/clash-linux-amd64-v1.7.1 -d ../clash/ > ~/.clash/out.log 2>&1 & 

clean :
	-rm .*.swp
	-rm ../.*.swp
