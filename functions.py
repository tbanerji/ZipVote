# wip functions file
from flask import (Flask, url_for, render_template, flash)
 
import cs304dbi as dbi
 
app = Flask(__name__)

"""Will return all the zipcodes that match the search term"""
def ziplist(searched,conn):
    curs=dbi.dict_cursor(conn)
    searched="%"+searched+"%"
    curs.execute('''select * from zipcodes where zipcode like %s''', searched)
    temp = curs.fetchall()
    return temp

"""Will return all the people who match the search term"""
def plist(searched,conn):
    curs=dbi.dict_cursor(conn)
    searched="%"+searched+"%"
    curs.execute('''select * from politicians where name like %s''', searched)
    temp = curs.fetchall()
    return temp

"""Returns list of all politicians in database"""
def polist(conn):
    curs=dbi.dict_cursor(conn)
    curs.execute('''select * from politicians''')
    polist = curs.fetchall()
    return polist
    
"""For a given person_id, this will return all info on a  """
def pidinfo(nm, conn):
    curs=dbi.dict_cursor(conn)
    curs.execute('''select * from politicians where person_id = %s''', nm)
    temp = curs.fetchone()
    return temp

"""Will return all the info related to an office"""
def oidinfo(nm, conn):
    curs=dbi.dict_cursor(conn)
    curs.execute('''select * from offices where o_id = %s''', nm)
    temp = curs.fetchone()
    temp['heldbyname'] = pidinfo(temp['heldby'],conn)['name']
    return temp

"""Table with info on causes and policies supported by a politician"""
def policies(pid,conn):
    curs=dbi.dict_cursor(conn)
    curs.execute('''select * from policies where person_id=%s''',pid)
    temp = curs.fetchall()
    return temp

"""presents info on a specific zipcode"""
def zipcodeinfo(zc, conn):
    curs=dbi.dict_cursor(conn)
    curs.execute('''select * from zipcodes where zipcode=%s''',int(zc))
    temp = curs.fetchone()
    return temp

"""gives info on an office"""
def addpos(info,conn):
    curs=dbi.dict_cursor(conn)
    curs.execute('''select * from offices where heldby=%s''',(info["person_id"]))
    temp = curs.fetchone()
    info['offname'] = temp['oname']
    info['offlink'] = url_for('office', num = temp['o_id'])
    return info

def politiciansforarea(zipcode,conn):
    curs = dbi.dict_cursor(conn)
    curs.execute('''select name,person_id from politicians 
    where person_id in 
    (select heldby 
    from offices inner join whovotes on (whovotes.o_id = offices.o_id) 
    where whovotes.zipcode = %s)''', zipcode)
    temp = curs.fetchall()
    return temp

"""Allows user to bookmark politician to their page"""
def addtolist(conn,username,person_id):
    curs=dbi.dict_cursor(conn)
    curs.execute('''select name from politicians where person_id=%s''',(person_id))
    name=curs.fetchone()
    name=name['name']
    curs.execute('''insert into user_favs(username,person_id,name,feeling) values (%s,%s,%s,%s)''', (username,person_id,name,'null'))
    conn.commit()
    
"""Allows user to update their stance on a politician"""
def update(conn,feelings,username,person_id):
    curs=dbi.dict_cursor(conn)
    curs.execute('''update user_favs set feeling=%s where person_id=%s and username=%s''',(feelings,person_id,username))
    conn.commit()

"""Lets user delete a politician from their bookmarked list """
def delete(conn,person_id,username):
    curs=dbi.dict_cursor(conn)
    curs.execute('''delete from user_favs where person_id=%s and username=%s''',(person_id,username))
    conn.commit()

def userfavs(conn,username):
    curs=dbi.dict_cursor(conn)
    curs.execute('''select * from user_favs where username=%s''',(username))
    temp = curs.fetchall()
    return temp
