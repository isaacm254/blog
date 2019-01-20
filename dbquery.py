import pymysql


class Operations:
    def __init__(self):
        self.connection = pymysql.connect(host="localhost", user="root", password="", database="DrSalwaBlog")
        self.cursor = self.connection.cursor()
        try:
            self.create_readings_table()
            self.create_article_table()
            self.create_sub_imgs_table()
            self.create_categories_table()
            self.create_article_classes_table()
            self.create_admin_table()
        except:
            print('error: tables already exist')

    def create_article_table(self):
        query = """CREATE TABLE article
        (id INTEGER PRIMARY KEY AUTO_INCREMENT,
        title VARCHAR(1000) NOT NULL,
        main_img VARCHAR(1000) NOT NULL,
        the_article TEXT NOT NULL,
        article_status INT(1) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME ON UPDATE CURRENT_TIMESTAMP)"""
        self.cursor.execute(query)

    def create_sub_imgs_table(self):
        query = """CREATE TABLE sub_imgs
        (id INTEGER PRIMARY KEY AUTO_INCREMENT,
        article_id INT NOT NULL,
        sub_img VARCHAR(1000) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME ON UPDATE CURRENT_TIMESTAMP)"""
        self.cursor.execute(query)

    def create_categories_table(self):
        query = """CREATE TABLE categories
        (id INTEGER PRIMARY KEY AUTO_INCREMENT,
        class_name VARCHAR(100) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME ON UPDATE CURRENT_TIMESTAMP)"""
        self.cursor.execute(query)

    def create_article_classes_table(self):
        query = """CREATE TABLE article_classes
        (id INTEGER PRIMARY KEY AUTO_INCREMENT,
        article_id INT NOT NULL,
        class_id INT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME ON UPDATE CURRENT_TIMESTAMP)"""
        self.cursor.execute(query)

    def create_admin_table(self):
        query = """CREATE TABLE admins
        (id INTEGER PRIMARY KEY AUTO_INCREMENT,
        username VARCHAR(100) NOT NULL UNIQUE,
        password VARCHAR(100) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME ON UPDATE CURRENT_TIMESTAMP)"""
        self.cursor.execute(query)

    def create_readings_table(self):
        query = """CREATE TABLE readings
        (id INTEGER PRIMARY KEY AUTO_INCREMENT,
        article_id INT NOT NULL,
        readings INT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME ON UPDATE CURRENT_TIMESTAMP)"""
        self.cursor.execute(query)

    def add_read(self, article_id):
        try:
            if self.check_if_read_exist(article_id):
                query = """UPDATE readings SET readings = readings + 1 WHERE article_id = {}""".format(article_id)
                self.cursor.execute(query)
                self.connection.commit()
                return True
            else:
                query = """INSERT INTO readings(article_id, readings) VALUES('{}', '1')""".format(article_id)
                self.cursor.execute(query)
                self.connection.commit()
                return True
        except Exception as e:
            return False    


    def check_if_read_exist(self, article_id):
        try:
            query = """SELECT * FROM readings WHERE article_id={}""".format(article_id)
            self.cursor.execute(query)
            count = self.cursor.rowcount
            if count:
                return True
            else:
                return False
        except Exception as e:
            return False
        

    def add_article(self, title, main_img, the_article, classes, sub_imgs):
        try:
            query = """INSERT INTO article(title, main_img, the_article, article_status) 
                    VALUES('%s', '%s', '%s', '1')""" % (title, main_img[0], the_article)
            self.cursor.execute(query)
            self.connection.commit()
            article_id = self.cursor.lastrowid
            blah1 = str(self.add_sub_imgs(article_id, sub_imgs))
            blah2 = str(self.add_article_classes(article_id, classes))
            return blah1 + blah2
        except Exception as e:
            return False
        

    def update_article(self, article_id, title, main_img, the_article, sub_imgs, classes):
        try:
            query = """UPDATE article 
            SET title = '%s',main_img = '%s', the_article= '%s' WHERE id = %s""" % (title, main_img[0], the_article, article_id)
            self.cursor.execute(query)
            self.connection.commit()
            blah1 = str(self.update_sub_imgs(article_id, sub_imgs))
            blah2 = str(self.update_classes(article_id, classes))
            return blah1 + blah2
        except Exception as e:
            return False
        

    def add_sub_imgs(self, article_id, sub_imgs):
        try:
            for sub_img in sub_imgs:
                query = """INSERT INTO sub_imgs(article_id, sub_img) VALUES('%s', '%s')""" % (article_id, sub_img)
                self.cursor.execute(query)
                self.connection.commit()
            return True
        except Exception as e:
            return False
            

    def update_sub_imgs(self, article_id, sub_imgs):
        try:
            deleted = self.delete_imgs_id(article_id)
            if deleted:
                for sub_img in sub_imgs:
                    query = """INSERT INTO sub_imgs(article_id, sub_img) VALUES('%s', '%s')""" % (article_id, sub_img)
                    self.cursor.execute(query)
                    self.connection.commit()
                return True
            else:
                return False       
        except Exception as e:
            return False
        

    def delete_imgs_id(self, article_id):
        try:
            query = """DELETE FROM sub_imgs WHERE article_id='%s'"""% (article_id)
            self.cursor.execute(query)
            return True
        except Exception as e:
            return False
        

    def update_classes(self, article_id, classes):
        try:
            deleted = self.delete_class(article_id)
            if deleted:
                for class_ in classes:
                    query = """INSERT INTO article_classes(article_id, class_id) VALUES('%s', '%s')""" % (article_id, class_)
                    self.cursor.execute(query)
                    self.connection.commit()
                return True
            else:
                return False
        except Exception as e:
            return False
        

    def delete_class(self, article_id):
        try:
            query = """DELETE FROM article_classes WHERE article_id='%s'"""% (article_id)
            self.cursor.execute(query)
            return True
        except Exception as e:
            return False
        

    def add_article_classes(self, article_id, classes):
        try:
            for class_id in classes:
                query = """INSERT INTO article_classes(article_id, class_id) VALUES('%s', '%s')""" % (article_id, class_id)
                self.cursor.execute(query)
                self.connection.commit()
            return True
        except Exception as e:
            return False
            

    def add_class(self, classe):
        try:
            query = """INSERT INTO categories(class_name) VALUES('%s')""" % (classe)
            self.cursor.execute(query)
            self.connection.commit()
            return True
        except Exception as e:
            return False

    def get_all_classes(self):
        try:
            query = """SELECT * FROM categories"""
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return rows
        except Exception as e:
            return False
        

    def login(self, username, password):
        try:
            query = """SELECT id FROM admin WHERE user_name='%s' AND password='%s'""" % (username, password)
            self.cursor.execute(query)
            row = self.cursor.fetchall()
            return row[0][0]
        except Exception as e:
            return False
        

    def get_articles(self, from_, id_):
        try:
            query = """SELECT * FROM article WHERE article_status = 1 AND created_at >= '%s' AND id > '%s' ORDER BY created_at DESC LIMIT 10"""% (from_, id_)
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            new_rows = self.get_sub_imgs_and_reads(rows)
            return new_rows
        except Exception as e:
            return False
        

    def get_sub_imgs_and_reads(self, rows):
        try:
            new_rows = []
            for row in rows:
                query = """SELECT sub_img FROM sub_imgs WHERE article_id = %s"""% (row[0])
                self.cursor.execute(query)
                imgs_rows = self.cursor.fetchall()
                reads = self.get_reads(row[0])
                classes = self.getClasses(row[0])
                new_rows.append({'row': row,
                    'sub_imgs': imgs_rows,
                    'readings': reads,
                    'classes': classes})
            return new_rows
        except Exception as e:
            return False
        

    def get_reads(self, article_id):
        try:
            query = """SELECT readings FROM readings WHERE article_id = %s"""% (article_id)
            self.cursor.execute(query)
            reads = self.cursor.fetchall()
            return reads[0][0]
        except Exception as e:
            return 0

    def getClasses(self, article_id):
        try:
            query = """SELECT class_id FROM article_classes WHERE article_id = '%s'"""% (article_id)
            self.cursor.execute(query)
            classes_id = self.cursor.fetchall()
            _classes_id = []
            classes = self.getClasses_from_id(classes_id)
            return classes
        except Exception as e:
            return False
        

    def getClasses_from_id(self, classes_id):
        try:
            classes = []
            for class_id in classes_id:
                query = """SELECT id, class_name FROM categories WHERE id = %s"""% (class_id[0])
                self.cursor.execute(query)
                name = self.cursor.fetchall()
                elem = [name[0][0], name[0][1]]
                classes.append(elem)
            return classes
        except Exception as e:
            return False
        

    def get_article(self, id_):
        try:
            query = """SELECT * FROM article WHERE id='%s' AND article_status = 1"""% (id_)
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            new_rows = self.get_sub_imgs_and_reads(rows)
            return new_rows
        except Exception as e:
            return False
        

    def get_articles_for_main(self, from_):
        try:
            query = """SELECT * FROM article WHERE article_status = 1 AND created_at >= '%s' ORDER BY created_at DESC LIMIT 3"""% (from_)
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            new_rows = self.get_sub_imgs_and_reads(rows)
            return new_rows
        except Exception as e:
            return False
        

    def get_most_readed(self):
        try:
            query = """SELECT article_id FROM readings ORDER BY readings DESC LIMIT 10"""
            self.cursor.execute(query)
            articles_id = self.cursor.fetchall()
            print(articles_id)
            articles = []
            for article in articles_id:
                row = self.get_article(article[0])
                if row:
                    articles.append(row[0])
            return articles
        except Exception as e:
            return False
        
    def get_newest(self):
        try:
            query = """SELECT * FROM article WHERE article_status = 1 ORDER BY created_at DESC LIMIT 10"""
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            new_rows = self.get_sub_imgs_and_reads(rows)
            return new_rows
        except Exception as e:
            return False
        

    def delete_article(self, article_id):
        try:
            query = query = """UPDATE article SET article_status = 0 WHERE id = '%s'"""% (article_id)
            self.cursor.execute(query)
            self.connection.commit()
            return True
        except Exception as e:
            return False
        

    def search(self, s_query):
        try:
            query = """SELECT * FROM article WHERE article_status = 1 AND title LIKE '%{}%' OR the_article LIKE '{}'""".format(s_query, s_query)
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            new_rows = self.get_sub_imgs_and_reads(rows)
            return new_rows
        except Exception as e:
            return False
        
