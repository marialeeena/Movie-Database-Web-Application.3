# ----- CONFIGURE YOUR EDITOR TO USE 4 SPACES PER TAB ----- #
import sys,os
sys.path.append(os.path.join(os.path.split(os.path.abspath(__file__))[0], 'lib'))
import pymysql

def connection():
    ''' User this function to create your connections '''    
    con = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='elena2806', db='movies') #update with your settings
    
    return con

def updateRank(rank1, rank2, movieTitle):

    # Create a new connection
    con=connection()

    # Create a cursor on the connection
    cur=con.cursor()
        
    try:
        rank1=float(rank1)
    except ValueError:
        return [("status",), ("error",)]
    
    try:
        rank2=float(rank2)
    except ValueError:
        return [("status",), ("error",)]
        
        
    try:    
        
        
        
        
        
        if (0 <= rank1 <= 10 and 0 <= rank2 <= 10):
            
            
            cur.execute("SELECT movie_id, `rank` FROM movie WHERE title = %s", (movieTitle,)) #the %s  expects a single value or a tuple of values. 
            #without the tuple, the method might not interpret the single value correctly, leading to errors. 
            #the comma in (movieTitle,) specifically denotes a tuple with one element, distinguishing it from just a parenthesized expression.
            #the quotes around rank are used to clarify we dont refer to the reserved keyword rank
            
            movies = cur.fetchall()   #cur.fetchall() retrieves all rows that the query returned.
            #it also returns a list of tuples, where each tuple represents a row from the result set.
            #movies is a list where each item is a tuple representing a row from the result set of the query. 
            #Each tuple contains the values for movie_id and rank for a movie with the specified title.
            
            
            if len(movies) == 1:
                
                movieid, currentrank = movies[0]   #unpacking the first (only) tuple into two variables
                if currentrank is not None:
                    newrank = (currentrank+rank1+rank2)/3
                else:
                    newrank = (rank1+rank2)/2
                cur.execute("UPDATE movie SET `rank` = %s WHERE movie_id = %s", (newrank, movieid))
                con.commit()
                
            else:
                return [("status",), ("error",)]
                
                
        else:
            return [("status",), ("error",)]
        
        
        
        print(rank1, rank2,movieTitle)
        return [("status",), ("ok",)]      #the comas here also show that we return a list of tuples and not just a string 
        
        
        
    except pymysql.MySQLError as error:    #error variable contains the instance of the pymysql.MySQLError exception that was raised
        print(f"Error: {error}")           #f-strings provide a way to embed expressions inside strings using curly braces
        return [("status",), ("error",)]
        
        
#example 
#result = updateRank(8, 10, "Fargo")
#print(result)  #should print the status which is what updateRank returns
 















def colleaguesOfColleagues(actorId1, actorId2):

    # Create a new connection
    con=connection()

    # Create a cursor on the connection
    cur=con.cursor()



    try:
        
        cur.execute("SELECT movie_id FROM role WHERE actor_id = %s", (actorId1,))   #when you execute a SELECT query using cur.execute(), the result set returned by the query consists of rows
        movies_of_a = cur.fetchall()                                                #the fetchall() method returns a list of tuples, each tuple has each rows' elements

        
        cur.execute("SELECT movie_id FROM role WHERE actor_id = %s", (actorId2,))
        movies_of_b = cur.fetchall()

        
        


        colleagues_by_movie_a = []                                                #list to store colleagues for each movie actor A has acted in
        for movie_id_tuple in movies_of_a:
            cur.execute("SELECT actor_id FROM role WHERE movie_id = %s", (movie_id_tuple[0],)) #it now takes the first and only element of the tuple movie_id_tuple which has the actor_id
            colleagues_of_a = cur.fetchall()
            colleagues_by_movie_a.extend(colleagues_of_a)                                      #this list gets extended meaning we add all the returned new tuples to it 

        colleagues_by_movie_b = []                                                #list to store colleagues for each movie actor B has acted in
        for movie_id_tuple in movies_of_b:
            cur.execute("SELECT actor_id FROM role WHERE movie_id = %s", (movie_id_tuple[0],))
            colleagues_of_b = cur.fetchall()
            colleagues_by_movie_b.extend(colleagues_of_b)
            
            
            
            
        query = '''
            SELECT title
            FROM movie
            WHERE movie_id IN (
                SELECT movie_id
                FROM role
                WHERE actor_id = %s
            ) AND movie_id IN (
                SELECT movie_id
                FROM role
                WHERE actor_id = %s
            )
        '''
        
        
        
        
        
        
        

        
        
        common_movies_all = set()   #use a set to ensure unique entries
        for tuple_a in colleagues_by_movie_a:
            for tuple_b in colleagues_by_movie_b:
                if tuple_a[0]!=tuple_b[0]  and tuple_a[0]!=actorId1 and tuple_a[0]!=actorId2 and tuple_b[0]!=actorId1 and tuple_b[0]!=actorId2 :  #assuming that the combinations M-1-2-a-b and M-2-1-a-b are different
                        cur.execute(query, (tuple_a[0], tuple_b[0]))
                        common_movies = cur.fetchall()
                        for movie in common_movies:
                            common_movies_all.add((movie[0], tuple_a[0], tuple_b[0], actorId1, actorId2)) #adding a new tuple to the list that has all these variables in it 


        #rows = len(common_movies_all)  #get the number of unique rows
        #print("rows:", rows)
        
        
        
        
        
        
        
        
        
        
        
        
        
        print (actorId1, actorId2)
        return [("movieTitle", "colleagueOfActor1", "colleagueOfActor2", "actor1","actor2")] + list(common_movies_all)   #concating the set to a list, both return values need to be lists
        
        
        
        
        
        
        
        
    except pymysql.MySQLError as error:    
        print(f"Error: {error}")           
        return [("status",), ("error",)]   
    
    
    
    
    
#example 
#result = colleaguesOfColleagues(376249, 22591)   #3236
#result = colleaguesOfColleagues(26409, 89558)    #4
#print(result)  #should print the return
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


def actorPairs(actorId):

    # Create a new connection
    con=connection()

    # Create a cursor on the connection
    cur=con.cursor()


    #finding all his genres 
    query='''                                       
        SELECT  DISTINCT g.genre_name
        FROM    actor a,role r,movie m,genre g,movie_has_genre mhg
        WHERE   a.actor_id=%s
            AND a.actor_id=r.actor_id
            AND m.movie_id=r.movie_id
            AND g.genre_id=mhg.genre_id
            AND mhg.movie_id=m.movie_id
    '''
    cur.execute(query,(actorID,))
    genres_of_a=cur.fetchall()
    
    #now we have to find the genres of all others actors..actually just for the actors he has collaborated with 
    #because its necessary for them to have worked together at least once 
    #so now lets find his colleagues and their genres 
    
    query='''
        SELECT    DISTINCT a2.actor_id,g2.genre_name
        FROM      actor a1,actor a2,role r1,role r2,movie m,genre g, movie_has_genre mhg
        WHERE     a1.actor_id=%s
            AND   a2.actor_id != %s
            
            AND   a1.actor_id=r1.actor_id
            AND   m.movie_id=r1.movie_id 
            
            AND   r1.movie_id=r2.movie_id
            
            AND   a2.actor_id=r2.actor_id 
            AND   m.movie_id=r2.movie_id
            
            AND g.genre_id=mhg.genre_id
            AND m.movie_id=mhg.movie_id
    '''
    
    cur.execute(query,(actorID,))
    genres_of_cols_of_a=cur.fetchall()  #if actor A has acted in both drama and comedy movies,the query will return two tuples: (actor_id, 'drama') and (actor_id, 'comedy')
    
    
    valid_actors=[]
    
    
    
    
    
    
    
    
    print (actorId)
    return [("actorId",),] + list(valid_actors)
    
    
    
    
    except pymysql.MySQLError as error:
        print(f"Error: {error}")
        return [("status",), ("error",)]


#example
result = actorPairs(22591)   #4
print(result)














    
    
    
def selectTopNactors(n):
    

    # Create a new connection
    con=connection()

    # Create a cursor on the connection
    cur=con.cursor()
    
    n = int(n)
    print (n)

    cur.execute("SELECT genre_name from genre order by genre_name")      

    genre_results = cur.fetchall()

    results =  [("genreName", "actorId", "numberOfMovies"),]   #initializing the results list with a tuple representing the header row containing column names 

    for row in genre_results:                                  #it loops through each genre 
        genre_name = row[0]                                    #the first item of the rowth tuple of the genre_results list is this genre's name
                                                               #for each genre, it executes an SQL query to retrieve the top N actors based on the number of movies they have appeared in for that genre

        cur.execute("""SELECT                                  
                genre.genre_name,
                actor.actor_id,
                count(distinct movie.movie_id)
            FROM
                movie,
                `role`,
                actor,
                movie_has_genre,
                genre
            where
                movie.movie_id = role.movie_id
                and role.actor_id = actor.actor_id
                and movie.movie_id = movie_has_genre.movie_id
                and movie_has_genre.genre_id = genre.genre_id
                and genre_name = %s
            group by
                actor.actor_id,
                genre.genre_id,
                genre.genre_name
            order by
                genre.genre_name asc,
                count(distinct movie.movie_id) desc,
                actor.actor_id asc 
        """, (genre_name,))
                    
        genre_results = cur.fetchall()

        i = 0                           #counting how many top actors we have found 

        for r in genre_results:
            results.append(r)
            i=i+1

            if i >= n:                  #when we have already found n actors, the inside for loop breaks
                break


    return results;
    
    
    except pymysql.MySQLError as error:
        print(f"Error: {error}")
        return [("status",), ("error",)]
    
    
    
#example 
#result = selectTopNactors(3) #photo
#print(result)  #should print the return   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

def traceActorInfluence(actorId):
    # Create a new connection
    con=connection()

    # Create a cursor on the connection
    cur=con.cursor()


    return [("influencedActorId",),]
