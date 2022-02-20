


import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import networkx as nx
from pyvis.network import Network

data=pd.read_csv("data/FlipKartCleaned.csv")
st.title('Phones Recommendation using Knowledge Graphs')

Name=list(data["Name"])
Rating=list(data["Rating"])
Battery=list(data["Battery"])
Processor=list(data["Processor"])
data["Price"] = data["Price"].str.replace("₹",'Rupees ')
Price=list(data["Price"])
RAM=list(data["RAM"])
Brand=list(data["Brand"])
Index=list(data["index"])
AdditionalDetails=list(data["AdditionalDetails"])

graph = Network(height='600px', width='100%', bgcolor='#222222', font_color='white')
g=nx.MultiDiGraph()
pos= nx.planar_layout(g)

edge_data = zip(Name,Brand,RAM,Processor,Rating,Index,Battery,AdditionalDetails,Price)

for e in edge_data:
    g.add_node(e[0],size=10,color="blue",id=e[5])
    g.add_node(e[1],size=30,color="yellow")
    g.add_node(e[2],size=10,color="blue")
    g.add_node(e[3],size=10,color="blue")
    g.add_node(e[6],size=10,color="blue")
    g.add_node(e[7],size=10,color="blue")
    g.add_node(e[8],size=10,color="blue")
    # graph.add_edge(src, dst, value=w)
    g.add_edge(e[0],e[1],title="Brand",color="white",length=300,weight=e[4])
    g.add_edge(e[0],e[2],title="RAM",color="red",weight=e[4],length=500)
    g.add_edge(e[0],e[3],title="Processor",color="yellow",length=600,weight=e[4])
    g.add_edge(e[0],e[6],title="Battery",color="yellow",length=600,weight=e[4])
    g.add_edge(e[0],e[7],title="Additional Details",color="yellow",length=600,weight=e[4])
    g.add_edge(e[0],e[8],title="Price",color="yellow",length=600,weight=e[4])

query_new=st.text_input("Enter search query with each specification separated by space for example - brand ram,like poco 8 gb ram  ","samsung 4 gb ram")
# query_new=st.text_input("Enter search query separated by space","samsung 4",on_change=st.experimental_rerun())
query=query_new.capitalize()
query=query.split()

fixing_details={}
# names=[]
for i in g.edges(data=True):
  for j in query:
    if j==i[1] and i[2]["title"]=="Brand":
      fixing_details["Brand"]=i[1]
    if j.isdigit() and i[2]["title"]=="RAM" and (j+" "+"GB"+" "+"RAM")==i[1]:
      fixing_details["RAM"]=i[1]
    if j.isdigit() and i[2]["title"]=="Processor" and j in i[1].split():
      print(i[1])
      fixing_details["Processor"]=i[1]
    if j.isdigit() and i[2]["title"]=="Battery" and (j+" "+"mAh Lithium-ion Battery")==i[1]:
      fixing_details["Battery"]=i[1]

name={}

for i in g.edges(data=True):
  test={}
  flag=0

  for nbr, datadict in g.adj[i[0]].items():
    for x in fixing_details.keys():
      if datadict[0]["title"]==x:
        if fixing_details[x]!=nbr:
          flag=1
          test={}
          # print("Flag is 1")
        else:
          # print(x)
          # print("Found Match",nbr)
          test[x]=nbr
          test["Rating"]=datadict[0]["weight"]
      
    test[datadict[0]["title"]]=nbr
    
  if flag==0:
    # print("Flag is not 1")
    # test["Name"]=i["from"]  
    name[i[0]]=test

stop=0
if name=={}:
  st.text("No Products found")
  stop=1

name_list=[]
ratings={}
for i in name:
  if stop==1:
    break
  # print(i)
  ratings[i]=name[i]["Rating"]
  name_list.append(i)


name_list=sorted(name_list, key=lambda x: ratings[x],reverse=True)

# print(ratings)
count=st.number_input("Enter how many search results you would like to see: ",5,10,5)
message_text="Showing first "+str(count)+" results "
st.subheader(message_text)
for i in name_list:
  if stop==1:
    break
  if count==0:
    break
  else:
    message_text="Name :"+str(i)
    st.text(message_text)
    message_text="Brand : "+str(name[i]["Brand"])
    st.text(message_text)
    message_text="Rating : "+str(name[i]["Rating"])
    st.text(message_text)
    message_text="RAM : "+str(name[i]["RAM"])
    st.text(message_text)
    message_text="Processor : "+str(name[i]["Processor"])
    st.text(message_text)
    message_text="Battery : "+str(name[i]["Battery"])
    st.text(message_text)
    message_text="Additional Details : "+str(name[i]["Additional Details"])
    st.text(message_text)
    message_text="Price : "+str(name[i]["Price"])
    st.text(message_text)
    st.text("\n")
    st.text("\n")
    count-=1
  st.text("\n")

# for i in name_list:
#   for j in name_list:
#     if i!=j:
#       g.add_edge(i,j,title="RelatedProducts",color="yellow",length=600,weight=e[4])

# graph.from_nx(g)

# print(len(name_list))



# nx.draw(g)

st.header("Showing Graph for all Related Products to the Search query (Restricted to 90 Products)")
graph1 = Network(height='600px', width='100%', bgcolor='#222222', font_color='white')

# set the physics layout of the network
g1=nx.MultiDiGraph()
pos= nx.planar_layout(g1)


for i in name_list[:90]:
  if stop==1:
    break
  g1.add_node(i,size=20,color="blue")

for i in name_list[:90]:
  for j in name_list:
    if stop==1:
      break
    if i!=j:
      g1.add_edge(i,j,title="RelatedProducts",color="red",length=1000)

# nx.draw(g1)
if stop!=1:
    graph1.from_nx(g1)

# graph1.show("graph.html")
# display(HTML("graph.html"))

if stop!=1:
        try:
            path = '/tmp'
            graph1.save_graph(f'{path}/pyvis_graph.html')
            HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

        # Save and read graph as HTML file (locally)
        except:
            path = '/html_files'
            graph1.save_graph(f'{path}/pyvis_graph.html')
            HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

# Load HTML file in HTML component for display on Streamlit page
components.html(HtmlFile.read(), height=600)

spec = st.radio(
     "To see other recommendations with different Brand,RAM or Battery capacity.Select the specification below.",
     ('Brand', 'RAM', 'Battery'))

def show(spec):
  name={}
  for i in g.edges():
    test={}
    flag=0
    for nbr, datadict in g.adj[i[0]].items():
      for x in fixing_details.keys():
        if x==spec:
          if datadict[0]["title"]==x:
            if fixing_details[x]!=nbr:
              test[x]=nbr
            else:
              flag=2

            
        else:
          if flag==2:
            break
          if datadict[0]["title"]==x:
            if fixing_details[x]!=nbr:
              flag=1
              test={}
          # print("Flag is 1")
          else:
            test[x]=nbr
            # print(nbr)
            test["Rating"]=datadict[0]["weight"]
      
      test[datadict[0]["title"]]=nbr
  
    if flag==0:
    # print("Flag is not 1")
    # test["Name"]=i["from"]
    # print(test)  
      name[i[0]]=test

  name_list=[]
  ratings={}
  if name=={}:
    message_text="No Recommendations for different"+spec
    st.text(message_text)
    stop=1
    return(stop)
    
  
  for i in name:
    ratings[i]=name[i]["Rating"]
    name_list.append(i)


  name_list=sorted(name_list, key=lambda x: ratings[x],reverse=True)

  message_text=" Showing other recommendations for "+str(spec)
  st.text(message_text)

  brandlist={}
  for i in name_list:
    if name[i][spec] not in brandlist.keys():
      message_text="Name :"+str(i)
      st.text(message_text)
      message_text="Brand : "+str(name[i]["Brand"])
      st.text(message_text)
      brandlist[name[i][spec]]=1                                   
      message_text="Rating : "+str(name[i]["Rating"])
      st.text(message_text)
      message_text="RAM : "+str(name[i]["RAM"])
      st.text(message_text)
      message_text="Processor : "+str(name[i]["Processor"])
      st.text(message_text)
      message_text="Battery : "+str(name[i]["Battery"])
      st.text(message_text)
      message_text="Additional Details : "+str(name[i]["Additional Details"])
      st.text(message_text)
      message_text="Price : "+str(name[i]["Price"])
      st.text(message_text)
      st.text("\n")
      st.text("\n")
                                           
    elif name[i][spec] in brandlist.keys() and brandlist[name[i][spec]]>2:
      pass
    elif name[i][spec] in brandlist.keys() and brandlist[name[i][spec]]>0 :
      message_text="Name :"+str(i)
      st.text(message_text)
      message_text="Brand : "+str(name[i]["Brand"])
      st.text(message_text)
      brandlist[name[i][spec]]=brandlist[name[i][spec]]+1
      message_text="Rating : "+str(name[i]["Rating"])
      st.text(message_text)
      message_text="RAM : "+str(name[i]["RAM"])
      st.text(message_text)
      message_text="Processor : "+str(name[i]["Processor"])
      st.text(message_text)
      message_text="Battery : "+str(name[i]["Battery"])
      st.text(message_text)
      message_text="Additional Details : "+str(name[i]["Additional Details"])
      st.text(message_text)
      message_text="Price : "+str(name[i]["Price"])
      st.text(message_text)
      st.text("\n")
 
  
  message_text="Showing Graph for other recommendations for" +spec+" (Restricted to 90 products)"                                         
  st.header(message_text)
  graph2 = Network(height='600px', width='100%', bgcolor='#222222', font_color='white')

# set the physics layout of the network
  g2=nx.MultiDiGraph()
  pos= nx.planar_layout(g2)


  for i in name_list[:90]:
    g2.add_node(i,size=20,color="blue")
  

  for i in name_list[:90]:
    for j in name_list[:90]:
      if i!=j:
        g2.add_edge(i,j,title="Other"+"Brand",color="red",length=1000)


  graph2.from_nx(g2)

  



  try:
    path = '/tmp'
    graph2.save_graph(f'{path}/pyvis_graph2.html')
    HtmlFile = open(f'{path}/pyvis_graph2.html', 'r', encoding='utf-8')

    # Save and read graph as HTML file (locally)
  except:
    path = '/html_files'
    graph2.save_graph(f'{path}/pyvis_graph2.html')
    HtmlFile = open(f'{path}/pyvis_graph2.html', 'r', encoding='utf-8')

    # Load HTML file in HTML component for display on Streamlit page
  components.html(HtmlFile.read(), height=600)
  return(2)

if show(spec)==1:
    pass
else:
    pass
