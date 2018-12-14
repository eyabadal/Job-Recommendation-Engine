import matplotlib 
matplotlib.use('Agg')
import igraph 
import requests
from igraph import *
from flask import Flask, render_template, send_file
import psycopg2
import agensgraph
from flask import Flask
from flask import Flask, render_template
import json
import cgi
from flask import request
import re
from collections import Counter,OrderedDict
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import random
import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from io import BytesIO
from flask import Flask, session


################# DB Connections ###################################

conn = psycopg2.connect("dbname=jobs host=127.0.0.1 user=eyabadal")
cur = conn.cursor()
#cur.execute("DROP GRAPH t CASCADE;") dbname=eya teh previouse one
#cur.execute("CREATE GRAPH t")
cur.execute("SET graph_path = skills")
conn.commit();

##################################### Flask Connections #############################################################
#name=str(v.props['id'])
app = Flask(__name__)


@app.route('/')
def stanford_page():
	return render_template('index.html')


@app.route('/login')
def login():
	return render_template('login.html')


@app.route('/test')
def test():
	return render_template('formWithFilter.html')











@app.route('/image/')
def graph_draw():
	n=session.get("n",None)
	nv=session.get("numberVertex",None)
	lablename=session.get("search",None)
	userSearchJob=session.get("searchskill",None)
	ln=session.get("skillNameTest",None)
	s=session.get("size",None)
	#G=nx.MultiGraph()
	G=nx.Graph()

	nodecolorsize=s


	for i in range(s):
		G.add_edge(userSearchJob,ln[i])

	nx.draw(G,with_labels = True, node_size=1800,font_size=8 ,edge_color="green",arrowsize=50,node_color=range(len(G)),cmap=plt.cm.Blues)
	img = BytesIO() # file-like object for the image
	
	plt.savefig(img,dpi=120) # save the image to the stream
	img.seek(0) # writing moved the cursor to the end of the file, reset
	plt.clf() # clear pyplot
	return send_file(img, mimetype='image/png')

	


#************************************************** Fetching *******************************************************************************
	

@app.route("/", methods=["GET","POST"])
def main():
#********************   name&age   *********************************
	#cur.execute("MATCH (n:person) RETURN n.name,n.age")
	cur.execute("MATCH (x:job) RETURN DISTINCT x.job_class;")
	newlist=[]
	paragraph=[]
	for record in cur:
		newlist.append(str(record));
	paragraph=newlist

	rs = newlist[0:]

#**********************  All Data  *********************************

	job_title=""
	a=[]
	dict_weighted_skills_by_job_ad={}
	skill_search=""

#**********************  HTML FORM   *********************************
#@app.route('/search/', methods=["GET","POST"])
#def search():


#***************************** Getting inputs form user *************************
	if request.method== "POST":
		#job_title = request.form['searchbox']
		skill_search = request.form['searchskillbox']
		session['searchskill'] = request.form['searchskillbox']

		choice=request.form.get("choice")

		session['city'] = request.form['city']
		city=session['city']


		state= request.form.get("stateChoice")




	w=[]
	v=[]

	for r in rs:
		w.append(str(r));
	v=str(w)

	s = re.sub('[^A-Za-z]', ' ', v)
	v=s[:]
	h=""
	num_supplements_for_job_class=""
	num_job_ads_for_job_class=""






	if job_title in v:
		jt=job_title
		cur.execute("MATCH (x:job) WHERE x.job_class='{}' and x.city='{}' RETURN count(x) limit 30;".format(str(job_title),str(city)))
		num_job_ads_for_job_class = cur.fetchall()[0][0]


		#***************************** Returningn ***************************
		#Graph Modeling
		#get total number of job ads for job title and then store them in a dictinary structure and then you can display it in an easier way 

		cur.execute("MATCH (x:job) WHERE x.job_class='{}'RETURN count(x);".format(str(job_title)))
		
		session['n'] = cur.fetchall()[0][0]
		result_style="No Graph"


		cur.execute("MATCH (x:job)-[:is_supplemented_by]->(y:supplement)-[:supplements]->(z:skill) WHERE x.job_class='{}' RETURN DISTINCT z.id, count(DISTINCT y) order by count desc limit 30;".format(str(job_title)))
		num_job_titles_with_skills = cur.fetchall()
		#creating weighting
		weighted_skills_by_job_ad = [(i[0],round((i[1]*100)/float(num_job_ads_for_job_class),3)) for i in num_job_titles_with_skills]
		dict_weighted_skills_by_job_ad = {}
		dict_weighted_skills_by_job_ad = (dict_weighted_skills_by_job_ad)
		for i in weighted_skills_by_job_ad:
			dict_weighted_skills_by_job_ad[i[0]] = str(round(i[1],2))
			
			
		#\return {"Job Title": job_title,"Skills to include in job description and percent of job requisitions that have the skill": dict_weighted_skills_by_job_ad}
		#a=json.dumps(dict_weighted_skills_by_job_ad,sort_keys=True, indent=4)



	elif job_title == "":
		h="The Job Title does not Exist"

		
                          
	else:

		h="The Job Title does not Exist"

	"""cur.execute("MATCH (n) WHERE n.job_title = 'Software Developer' RETURN n.job_title")
	w=[]
	v=[]
	for r in cur:
		w.append(str(r));
	v=str(w)

		s = re.sub('[^A-Za-z]', '', v)
		v=s[1:]



		if w==title:
			result = "The person is currently in our system "

	"""

#********************** Graph Visualization ***********************
	#cur.execute("MATCH (a:skill)<-[:supplements]-(supplement)<-[:is_supplemented_by]-(x:job)-[:is_supplemented_by]->(supplement)-[:supplements]->(b:skill) WHERE a<>b AND a.id = 'c' AND x.job_class = 'Engineering' RETURN count(supplement);")
	#num= cur.fetchall()[0][0]

#************************ Search For Skill by entering Job Class *************************************************************
#*********************************************************************************************************************************
#*********************************************************************************************************************************

	if skill_search in v and choice == "skill":
		cur.execute("MATCH (x:job)-[r:requires]->(z:skill) WHERE x.job_class='{}' and x.city='{}' RETURN DISTINCT x,r,z limit 30 ;".format(str(skill_search),str(city)))

		data=cur.fetchall()
		jobNum=""
		
		#session[vertexName]=cur.execute("MATCH (x:job)-[r:requires]->(z:skill) WHERE x.job_class='Engineer' RETURN DISTINCT x.job_title limit 10 ;".format(str(skill_search)))
		Num=str(data)
		if "Vertex" in Num:
			jobNum="Yes"
		session["numberVertex"]=Num.count("job[")
		session["numberSkills"]=Num.count("skill[")

		cur.execute("MATCH (x:job)-[r:requires]->(z:skill) WHERE x.job_class='{}' and x.city='{}' and x.state='{}' RETURN DISTINCT z.id limit 30 ;".format(str(skill_search), str(city), str(state)))
		skillName1=cur.fetchall()
		skillName2=re.sub('[^A-Za-z]', ' ', str(skillName1))
		session["skillName"]=wordList = re.sub("[^\w]", " ",  skillName2).split()
		
		#**************************** Weight ********************************************************************
		cur.execute("MATCH (x:job) WHERE x.job_class='{}' and x.city='{}' and x.state='{}' RETURN count(x) limit 30;".format(str(skill_search), str(city), str(state)))
		num_job_ads_for_job_class1 = cur.fetchall()[0][0]

		cur.execute("MATCH (x:job)-[:is_supplemented_by]->(y:supplement)-[:supplements]->(z:skill) WHERE x.job_class='{}' and x.city='{}' and x.state= '{}' RETURN DISTINCT z.id, count(DISTINCT y) order by count desc limit 30;".format(str(skill_search), str(city), str(state)))
		num_job_titles_with_skills1 = cur.fetchall()

		weighted_skills_by_job_ad1 = [(i[0],round((i[1]*100)/float(num_job_ads_for_job_class1),3)) for i in num_job_titles_with_skills1]

		dict_weighted_skills_by_job_ad1 = {}
		dict_weighted_skills_by_job_ad1 = (dict_weighted_skills_by_job_ad1)
		for i in weighted_skills_by_job_ad1:
			dict_weighted_skills_by_job_ad1[i[0]] = str(round(i[1],2))
		
		#weight=dict_weighted_skills_by_job_ad1.values()
		#weight1=weight[0]
		weight=[]
		for key in dict_weighted_skills_by_job_ad1.keys():
			weight.append(dict_weighted_skills_by_job_ad1[key])
		

		session["skillNameTest"]=[]
		for key in dict_weighted_skills_by_job_ad1.keys():
			session["skillNameTest"].append(key)

		items=session["skillNameTest"]
		if len(items) == 30:
			session['size']=(len(items)-1)
		else:
			session['size']=(len(items))

		
#********************************** Search For Supplements by entering Job Class **********************************************************
#*********************************************************************************************************************************
#*********************************************************************************************************************************

	if skill_search in v and choice == "supplement":
		data=0
		jobNum=0
		supplement=0
	

		cur.execute("MATCH (x:job) WHERE x.job_class='{}' and x.city='{}' RETURN count(x) limit 30;".format(str(skill_search), str(city)))
		num_job_ads_for_job_class1 = cur.fetchall()[0][0]

		cur.execute("MATCH (x:job)-[:is_supplemented_by]->(y:supplement) WHERE x.job_class='{}' and x.city='{}' RETURN DISTINCT y.job_title, count(DISTINCT y) order by count desc limit 30;".format(str(skill_search),str(city)))
		num_job_titles_with_skills1 = cur.fetchall()

		weighted_skills_by_job_ad1 = [(i[0],round((i[1]*100)/float(num_job_ads_for_job_class1),3)) for i in num_job_titles_with_skills1]


		dict_weighted_skills_by_job_ad1 = {}

		dict_weighted_skills_by_job_ad1 = (dict_weighted_skills_by_job_ad1)
		for i in weighted_skills_by_job_ad1:
			dict_weighted_skills_by_job_ad1[i[0]] = str(round(i[1],2))
		
		#weight=dict_weighted_skills_by_job_ad1.values()
		#weight1=weight[0]
		weight=[]
		for key in dict_weighted_skills_by_job_ad1.keys():
			weight.append(dict_weighted_skills_by_job_ad1[key])
		

		session["skillNameTest"]=[]
		for key in dict_weighted_skills_by_job_ad1.keys():
			session["skillNameTest"].append(key)

		items=session["skillNameTest"]


		session['size']=len(items)

#********************************** Search For Job_title by entering Job Class **********************************************************
#*********************************************************************************************************************************
#*********************************************************************************************************************************
	

	if skill_search in v and choice == "job":
		data=0
		jobNum=0
		supplement=0
	

		cur.execute("MATCH (x:job) WHERE x.job_class='{}' and x.city='{}' RETURN count(x) limit 30;".format(str(skill_search), str(city)))
		num_job_ads_for_job_class1 = cur.fetchall()[0][0]

		cur.execute("MATCH (x:job)-[:is_supplemented_by]->(y:supplement)-[:supplements]->(z:skill) WHERE x.job_class='{}' and x.city='{}' RETURN DISTINCT x.job_title, count(DISTINCT x) order by count desc limit 30;".format(str(skill_search), str(city)))
		num_job_titles_with_skills1 = cur.fetchall()

		weighted_skills_by_job_ad1 = [(i[0],round((i[1]*100)/float(num_job_ads_for_job_class1))) for i in num_job_titles_with_skills1]

		dict_weighted_skills_by_job_ad1 = {}
		dict_weighted_skills_by_job_ad1 = (dict_weighted_skills_by_job_ad1)
		for i in weighted_skills_by_job_ad1:
			dict_weighted_skills_by_job_ad1[i[0]] = str(round(i[1],2))
		
		#weight=dict_weighted_skills_by_job_ad1.values()
		#weight1=weight[0]
		weight=[]
		for key in dict_weighted_skills_by_job_ad1.keys():
			weight.append(dict_weighted_skills_by_job_ad1[key])
		

		session["skillNameTest"]=[]
		for key in dict_weighted_skills_by_job_ad1.keys():
			session["skillNameTest"].append(key)

		items=session["skillNameTest"]
		session['size']=len(items)










#********************************** Enter Skill and get related jobs   **********************************************************
#*********************************************************************************************************************************
#*********************************************************************************************************************************












	
		

	#return render_template('hometest.html',supplement=supplement)
	return render_template('hometest.html',h=h,rs=rs,num_supplements_for_job_class=num_supplements_for_job_class, dict_weighted_skills_by_job_ad1=dict_weighted_skills_by_job_ad1, a= session['n'], data=data ,jobNum=jobNum, nv=session["numberVertex"],skillNameTest=session["skillNameTest"],weight=weight,choice=choice, city=city)


#********************  Running the App  ***************************
if __name__ == "__main__":
	app.secret_key = 'some secret key'
	app.run(debug=True)





