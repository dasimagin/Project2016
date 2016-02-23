NAME = wiki-crawler.py
PID = $(NAME).pid

INIT = http://simple.wikipedia.org/wiki/Philosophy

prepare:
	mkdir -p html
	mkdir -p text

debug: prepare
	python3 $(NAME) --log=debug --thread-n=16 $(INIT)


# stop:
# 	if [ -e $(PID) ]; then \
# 		if [ -f /proc/'head -1 $(PIDFILE)'/status ];then \
# 		/sbin/start-stop-daemon --stop --signal 2 --pidfile $(PIDFILE) --retry 3 ;\
# 		rm -f $(PIDFILE); \
# 		fi; \
# 		fi
# 	rm -f nohup.out

# start: prepare stop
# 	nohup /sbin/start-stop-daemon -m --pidfile $(PID) \
# 		--start --startas $(NAME) --thread-n=16 $(INIT)&

clean:
	rm -rf .index .queue
	rm -rf html text
