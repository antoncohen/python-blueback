python-blueback
===============

**This project is abandoned and incomplete, though it does work. Use [Ruby gem backup](https://github.com/meskyanichi/backup) instead.**

python-blueback is a cloud backup utility, it backs up files on your server to cloud storage. Configurations are done in ini-style files. There is a `blueback` executable, it is designed to run from cron.

I had big plans for this, like backing up databases directly, backing up over SSH (rsync/sftp), and other stuff. Then I found the [Ruby gem backup](https://github.com/meskyanichi/backup) by Michael van Rooijen, which does everything I wanted blueback to do, except is doesn't use a nice machine writable config format. I may re-write all the config parsing in Ruby to make the backup gem use YAML or ini-style configs. That's why this is called 'python-blueback' and not 'blueback'.

## Configuration ##
By default python-blueback reads config files from /etc/blueback.conf and any .conf file in /etc/blueback.d/. You can pass `-c file.conf` on command line. Or pass arguments on command line, use `-h` or `--help` for a list of args.

python-blueback runs 'jobs', which are named in the ini section heads. The [main] section is inherited by all jobs.

```
[main]
destination_type=s3
destination_container=s3bucket.exmaple.com
destination_key=YOUR_S3_KEY
destination_secret=YOUR_S3_SECRET

# This job is named 'test'
[test]
# Path on the bucket (subfolder)
destination_path=/testbackup
# Prefix for the backup file
destination_prefix=backtests
# Path to source to backup
source_name=./backuptests
```

## Testing ##
```
git clone https://github.com/antoncohen/python-blueback.git
cd python-blueback
vim test.conf  # Enter your S3 bucket and creds
. pythonpath.sh  # Adds current dir to python path
bin/blueback -c test.conf test  # Runs the test job
```

* Anton Cohen <anton@antoncohen.com>
* [Source](https://github.com/antoncohen/python-blueback)
* [Homepage](http://www.antoncohen.com/)
* [@antoncohen](http://twitter.com/antoncohen)
