"""
File: FlickrCrawler.py
Version: 1.0
Author: Surender Kumar
Copyright @ *****
Contact: emailsurenderkumar@gmail.com

A Basic Flickr Crawler
======================
This is a small example to crawl the Flickr database, a social networking
website, and store the crawled data systematically into a MySQL database. This
is performed in the following manner.

This will automatcally create the DB. The default DB info can be changed in file
'SQLDB.py'. Also, the DB password is encrypted and corresponding cipher code
will be written to a file for future use. The default password can be changed
in the file 'EncDec.py', search for DB_PASSWD.

For the given user, this will download the following.
- their social contacts/links (i.e. Friends)
- IDs of photographs uploaded by users
- for each photo, the tags info, if any, associated by the user

This crawled data is populated into a MySQL database. It automatically creates
the both database and tables in following manner.
- Users' information will be stored into:
    user(userid, username)

- The information pertaining to social links between users' will be stored into:
    links(userid1, userid2)

- Table to store details of photos:
    photo(photoid, owner, title)

- Table to store tags associated with photo:
    tags(tagid, photoid, tag)

Please refer the README file for the steps to run this crawler.
"""

# coding: utf-8
import flickr
import MySQLdb
import Queue
import sys
import Logger
from SQLDB import MySQLDB

"""
Flickr user to explore the connection of and populate the DB. Because this is a
sample script, therefore, hardcoding the user and user-id.
"""
GIVEN_USER_ID = '59634928@N04'
GIVEN_USER = 'suren44'
# Maximum number of users that can be crawled
MAX_USERS = 4

class FlickrCrawler (object):
    def __init__(self, givenUsr, givenUsrId, maxUsrs):
        # To be automated
        self.theGivenUsr = givenUsr # User to explore the connection of
        self.theGivenUsrId = givenUsrId # User ID
        """
        Maximum number of supported users depend on the both DB size and
        business requirement, and can be regulated automatically.
        """
        self.nUsers = 0
        self.nMaxNumOfUsrSupp = maxUsrs
        self.expUsrs = [] # To skip processed users
        self.photoProcesd = [] # To skip processed photos and tags
        self.Que = Queue.Queue(0) # To process user's connections in BFS order
        self.logH = Logger.getLogger()
        # Lets initialize database
        self.mySQLDBObj = MySQLDB()
        self.mySQLDBObj = MySQLDB()
        self.dbName = self.mySQLDBObj.getSQLDBName()
        self.dbCursor = self.mySQLDBObj.cursor
        self.mySQLDBObj.createDB()
        self.mySQLDBObj.createTables()

    @property
    def log (self):
        return self.logH

    """
    @property
    def cursor (self):
        return self.dbCursor
    """

    """
    Insert user's photo info into the DB.
    """
    def insrtUsrPhoto (self, pId, uId, pTitle):
        # Preparing a mySQL query to insert photo into the DB
        insrtPhotoSQLDB = "INSERT INTO photo(" + "photoid" + "," + "owner" + \
                "," + "title" + ") \t"
        insrtPhotoSQLDB += "VALUES \t"
        insrtPhotoSQLDB += "(" + "'" + str(pId)+"'" + ", " + "'" + str(uId) + \
                "'" + ", " + "'" + str(pTitle) + "'" +" )"

        try:
            self.dbCursor.execute(insrtPhotoSQLDB)
            self.log.info("Inserted photo '" + (pId) + "' into database")
        except:
            self.log.info("Failed to insert photo '" + str(pId) + \
                    "' into database")
            exit(1)

    """
    Insert tag info associated with this photo into the DB.
    """
    def insrtPhotoTag (self, tId, pId, tagT):
        insrtTagsSQLDB = "INSERT INTO tags(" + "tagid" + "," + "photoid" + \
                "," + "tag" + ") \t"
        insrtTagsSQLDB +="VALUES \t"
        insrtTagsSQLDB +="(" + "'" + str(tId) + "'"+", " + "'" + str(pId) + \
                "'" + ", " + "'" + str(tagT)+"'" + ")"

        try:
            self.dbCursor.execute(insrtTagsSQLDB)
            self.log.info("Inserted tag: '" + tId + "' into tags table")
        except:
            self.log.error("Failed to insert tag '" + tId + "' into database.")
            exit(1)

    """
    This method will store Usr and its friend into 'links' table
    """
    def insrtUsrLink (self, uId, fId):
        insrtLinkSQLDB = "INSERT INTO links(" + "userid1" + "," + "userid2" + \
                ") \t"
        insrtLinkSQLDB +="VALUES \t"
        insrtLinkSQLDB +="('" + str(uId) + "'" + ", " + "'" + str(fId) + \
                "'" + " )"

        try:
            self.dbCursor.execute(insrtLinkSQLDB)
            self.log.info("Inserted user link (" + str(uId) + ", " +
                    str(fId) + ") into database.")
        except:
            self.log.error("Failed to insert user link (" + str(uId) +
                    ", " + str(fId) + ") into database.")
            exit(1)

    """
    This method will store Usr into 'user' table
    """
    def insrtUsr (self, uId, uName):
        insrtUser = "INSERT INTO user(" + "userid" + "," + "username" + ") \t"
        insrtUser += "VALUES \t"
        insrtUser += "(" + "'" + str(uId) + "'" + ", " + "'" + str(uName) + \
                "'" + " )"

        try:
            self.dbCursor.execute(insrtUser)
            self.log.info("Inserted user (" + str(uId) + ", " + str(uName) +
                    ") into database.")
        except:
            self.log.error("Failed to insert user (" + str(uId) + ", " +
                    str(uName) + ") into database.")
            exit(1)

    """
    This method will retrieve photos and tags of the user.
    """
    def PopulatePhotosAndTags (self, User, Photos):
        for photo in Photos:
            if not isinstance(photo, str) and not isinstance(User, str) and \
                    not (photo.id in self.photoProcesd):
                self.insrtUsrPhoto(photo.id, User.id, photo.title)
                self.photoProcesd.append(photo.id)
                # Retrieving Tags associated with this photo
                Tags = photo.tags

                # Lets store TAGID, PHOTOID and TAG into the database
                if not Tags: #By-pass if Tags list is empty
                    continue

                for tag in Tags:
                    self.insrtPhotoTag(tag.id, photo.id, tag.text)

    """
    Retrive immidiate friends of this user, i.e. at 0-hop, and enque them.
    """
    def PopulateUserConns (self, Usr, Friends):
        for friend in Friends:
            if not isinstance(friend, str) and not isinstance(Usr, str):
                self.insrtUsrLink(Usr.id, friend.id)

                if (self.nUsers < self.nMaxNumOfUsrSupp) and not (friend.id in
                        self.expUsrs):
                    # BFS : Enqueuing user-id of each friend of the Usr
                    self.Que.put(friend)
                    self.expUsrs.append(friend.id)
                    self.nUsers += 1
                    self.log.debug("Queue Size: " + str(self.Que.qsize()) + \
                            ", self.nUsers: " + str(self.nUsers))

    """
    Top/Wrapper method to explore the connections and fetch the data. It
    explores friends' of the user in BFS order.
    """
    def ExploreConnsAndRetData (self, U):
        if (self.nUsers >= self.nMaxNumOfUsrSupp):
            exit(0) # Limit exhausted, exit successfully.

        # Flickr API to retrieve list of Photos with UserID
        Photos = flickr.people_getPublicPhotos(U.id)

        if not Photos and not isinstance(U, str):
            self.log.debug("User: '" + U.id + "' has no photos")
        else:
            self.PopulatePhotosAndTags(U, Photos)

        # Storing the USERID and USERNAME into the database
        try:
            if not isinstance(U, str):
                self.insrtUsr(U.id, U.name)
        except:
            pass

        # Exploring friends' of the user
        if (self.nUsers < self.nMaxNumOfUsrSupp):
            FriendsList = flickr.contacts_getPublicList(U.id)

            if FriendsList:
                self.PopulateUserConns(U, FriendsList)

        if (self.Que.qsize() > 0) and (self.nUsers < self.nMaxNumOfUsrSupp):
                self.ExploreConnsAndRetData(self.Que.get())

if __name__ == '__main__':
    flikCrawObj = FlickrCrawler(GIVEN_USER, GIVEN_USER_ID, MAX_USERS)
    flikCrawObj.log.debug("Exploring the user: '" + flikCrawObj.theGivenUsr +
            "' with user-id: '" + flikCrawObj.theGivenUsrId + "'")
    flickrUserObj = flickr.User(flikCrawObj.theGivenUsrId,
            flikCrawObj.theGivenUsr)
    flikCrawObj.ExploreConnsAndRetData(flickrUserObj)
    flikCrawObj.mySQLDBObj.exitDB()
