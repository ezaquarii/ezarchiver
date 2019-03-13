# EZ Archiver - Yet Another Duplicity Wrapper

EA Archiver is a frontend for the duplicity backup tool.

Duplicity incrementally backs up files and folders into
tar-format volumes encrypted with GnuPG and places them to a
remote (or local) storage backend.

Duplicity is fairly popular tool and is available in most Linux
distributions.

http://duplicity.nongnu.org/

# Installation

### Make into a custom directory

You need a GNU Make.

```
$ make install DESTDIR=/opt/ezarchiver/
```

### Debian package

All dependencies are supplied in `pypi` directory in source form and
the build runs off-line. **No dependencies fetching from the internet!**

```
$ debuild -uc -us -b
$ sudo dpkg -i ../ezarchiver*.deb
```

# Honorable mention

I have to mention another tool that IMO does a great job as a `tar`
replacement:

http://dar.linux.free.fr/

Sadly, duplicity is not supporting it.

# Pain points - why I did this in the first place?

Duplicity packages available in Debian/Ubuntu have 2 significant
pain point:

1. no backends
2. packages are outdated

Documentation advises to uses `pip install` to add missing
backends, but this pollutes local `site-packages` and might
not be convenient in many environments.

EZ Archiver allows `virtualenv`-isolated deployment of
`duplicity` with some helper scripts on top of that.

I keep my backup on an encrypted external USB drive. I don't do any
"incremental", "tower of Hanoi" or any other fancy stuff on my
personal machine - it's just an archive with stuff I collected over
the years, fairy reasonable in size - big, but not even close to
`/r/datahoarder` scale.

My only concern was to add an off-site copy of this archive in a
convenient way and - sadly - none of the existing tools provided
me with a simplicity I expected.

There is plenty of very simple tools that do not add any value over
an USB stick and `rsync`/`cp`, and plethora of overcomplicated
swiss-army-axes that are more tedious to configure and maintain than
writing a purpose-build bash script.

# Supported backends

This tool supports only B2 (Back Blaze) backend. I don't use anything
else for now, but I have a prototype for Google Drive that uses
service accounts, if somebody is interested.

# Features

1. deployment in isolated `virtualenv`
2. `b2` cloud storage backend
3. backup configuration using profiles: `Archivefile` (inspired by other
   something-something-file, like `Dockerfile`, `Vagrantfile`, etc)
4. very simple
5. Python Wheel package

# Installation

Deploying EZ Archiver is very simple. Assuming `/opt/ezarchiver` is
writable by user (never run `Makefile` as `root`!):

```
$ make install DESTDIR=/opt/ezarchiver/
$ /opt/ezarchiver/bin/ezbackup --help
/opt/ezarchiver/bin/ezbackup --help
usage: backup.py [-h] [--allow-source-mismatch] TYPE ARCHIVEFILE

EZ Archiver

positional arguments:
  TYPE                  Type of backup, either full or incr
  ARCHIVEFILE           Backup job configuration file

optional arguments:
  -h, --help            show this help message and exit
  --allow-source-mismatch
                        Allow performing backup with changed source directory
```

# Making backups

`Archivefile` is a YAML file strictly following `duplicity` options.
This example has all features included:

```
b2:
  account_id: <your bucket account id>
  application_key: <your bucket auth key>
  bucket: <your bucket name>
  folder: /backups/foo
encrypt_key: <your gpg key id or e-mail>
root: /home/foo
exclude:
  - exclude_1
  - ...
include:
  - include_1
  - ...
```

`ezbackup` can be invoked with a path to `Archivefile` or a directory
where `Archivefile` is present.

## Example 1 - `Archivefile` inside archived directory `/home/ezaquarii`

Let's try to back up my home directory: `/home/ezaquarii`.

```
b2:
   ...skip...
encrypt_key: hello@ezaquarii.com
exclude:
  - .cache
  - .trash
```

Notice that the file has no `root` field - this will be detected
automatically from `/home/ezaquarii/Archivefile` path.

```
$ /opt/ezarchiver/bin/ezbackup full /home/ezaquarii
... archiving takes quite some time ...
... modify home ...
$ /opt/ezarchiver/bin/ezbackup incr /home/ezaquarii
... incremental backup takes less time ...
$ _
```

## Example 2 - `Archivefile` outside archived directory `/home/ezaquarii`

Let's try to back up my home directory: `/home/ezaquarii` using a file
stored in `/root/ezaquarii.archivefile`.

```
b2:
   ...skip...
encrypt_key: hello@ezaquarii.com
root: /home/ezaquarii
exclude:
  - .cache
  - .trash
```

Notice that the file has `root` field that points to some arbitrary
position.

```
# /opt/ezarchiver/bin/ezbackup full /root/ezaquarii.archivefile
...
# /opt/ezarchiver/bin/ezbackup incr /root/ezaquarii.archivefile
...
# _
```

# Restoring backup

Backup restoration is performed using `ezrestore` script. The
script requires the `Archivefile` profile.

## Example 3 - restoring backup

```
# /opt/ezarchiver/bin/ezrestore /root/ezaquarii.archivefile /home/ezaquarii
```

That's all!

# FAQ

### Why packaging whole virtualenv?

Dependencies shipped by distributions are older than I needed and
some are not packaged at all. Newest Duplicity is not even published
in PyPI!

### But duplicity has so many more features! Why U No Provide Them!

I simply don't need them. This is a purpose-built tool, optimized
for a specific use case.

### Why not FTP?

I'd rather prefer to use SSH / FTP instead of some proprietary
cloud storage, but the FTP hosting prices are ridiculous and I need
>20GB that you can usually find.

### Why not Google Drive?

Reliability is good and pricing is reasonable, but their
Linux API is so-so.

Their OAuth2 authentication require typing a password and service
account does not allow browsing files in web UI.

### Why not DropBox?

They charge per-1000GB and I don't need that.

### Why not Go?

Go away.

### Why not Node.js?

You too.

### Why B2?

Quite frankly they provided me with the best development experience
and they are on the market for some time already.

Their pricing is sensible too.

### Are you not concerned that the cheap provider may go away?

Yes, I do! Cloud storage cut-throat competition wiped out so many...
