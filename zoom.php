<html>
<head>
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <style>
    	body{
        width:100%;

        }
	    .class1{background-color: #FFFFFF;}
	    .class0{background-color: #CFCFCF;}
	    .author{width: 200px;}
	    table{width:100%;}
	    td{width:50px;}
        td.wide{width:100px;}
    </style>
    <script type="text/javascript" src="http://d3js.org/d3.v2.min.js"></script>
</head>
    <body>
    <?php
        if(isset($_POST['equation'])){
            print "<div class='equationRef'>Equation Set:    ";
            print $_POST['equation'];
            print "</div>";
            ?>
            <script>var equation='<?php echo $_POST['equation'];?>'</script>
            <?php
        }
        else{
            print "Please Enter a Sorting Equation";
            ?>
            <script>var equation="YR";</script>
            <?php
        }
    ?>
    <script>
    console.log(equation);
    var color = d3.scale.category20();
    function sortNumber(a,b){return theEquation(a)-theEquation(b);}
    function sortNumberBack(b,a){return theEquation(a)-theEquation(b);}
    var array_of_winners=[]
    function theEquation(a){
    	var YR=parseInt(a['average_year_published']);
    	var FA=parseInt(a['Number_Of_Papers_Written_First_Author']);
    	var SA=parseInt(a['Number_Of_Papers_Written_Second_Author']);
    	var C=parseInt(a['Total_Number_Of_Citations']);
    	var NP=parseInt(a['Number_Of_Papers_Written']);
    try{
    var answer=eval(equation);
            return answer;
        }
    catch(err){
    console.error(err)
            console.log("recognized error")
            return null;
        }
    }
    function visualizeData(array_of_winners){
        $(document).ready(function(){
            $("body").append("<div class='eqEnter'><br><p>Enter An equation to find the top scorers</p></div>");
            $("div.eqEnter").append("<form action='/D3_testing/zoom.php' method='POST'><input name='equation'></input><input type='submit'></input></form>")
            $("div.eqEnter").append("<p>Variables:<br>YR=year<br>FA= Number of Papers First Authored<br>SA=Number of Papers Second Authored<br>C=Total Number of Citations<br>NP=Number of Papers Authored<br>You can enter a name with no keywords</p>")
            $("body").append("<table></table>");
            $("table").append("<tr class='class2'><td class='wide'>Name</td><td class='wide'>Average Year Published</td><td class='wide'>Number of Papers Written</td><td class='wide'>Total Number of Citations</td><td class='wide'>Number First Authored</td><td class='wide'>Number Second Authored</td>")
            for(var i=0; i<array_of_winners.length; i+=1){
                $("body").append("<tr id='ID"+i+"' class='class"+i%2+"'>");
                $("#ID"+i).append("<td><a href='onlineProfile.php?name="+array_of_winners[i]["Author"]+"'>"+array_of_winners[i]['Author']+"</a></td><td></td>")
                $("#ID"+i).append("<td>"+array_of_winners[i]['average_year_published']+"</td><td></td>");
                $("#ID"+i).append("<td>"+array_of_winners[i]['Number_Of_Papers_Written']+"</td><td></td>");
                $("#ID"+i).append("<td>"+array_of_winners[i]['Total_Number_Of_Citations']+"</td><td></td>");
                $("#ID"+i).append("<td>"+array_of_winners[i]['Number_Of_Papers_Written_First_Author']+"</td><td></td>");
                $("#ID"+i).append("<td>"+array_of_winners[i]['Number_Of_Papers_Written_Second_Author']+"</td>");
            }
            })
                          
        
    }

//update the table data
    function updateTable(data){
        if(theEquation(data[0])||theEquation(data[0])===0){
        for(var i=0; i<data.length; i+=1){
            var score=theEquation(data[i]);
            if(array_of_winners.length==0)array_of_winners.push(data[i]);
            else if(score>theEquation(array_of_winners[0]) || array_of_winners.length<500){
                array_of_winners.push(data[i]);
                array_of_winners.sort(sortNumber);
                if (array_of_winners.length>500)array_of_winners.shift();
            }
        }
        array_of_winners.sort(sortNumberBack);
        }
        else{
            for(var a=0; a<data.length; a++){
                if(data[a]['Author'].indexOf(equation)>-1)
                    array_of_winners.push(data[a])
            }
        }
        return array_of_winners;
    }
            
        var global_color_index=0;
        function nodeMake(author){return {x: 50, y: 60, name: author, color: global_color_index}}
        function linkMake(theSource, theTarget){
            return {source: theSource, target: theTarget};
        }
        function nodeMakeFromList(nodes){
            new_nodes=[];
                
            for(var node=0; node<nodes.length; node+=1){
                new_nodes.push(nodeMake(nodes[node]));
                    
            }
            return new_nodes;
        }
            

// make the initial graph and instantiates all of the variables
	function updateGraph(data, array_of_winners){
        var ball_selected;
        var canvas=d3.select("body")
	                .append("svg")
	                .attr("width", 500)
	                .attr("height", 500)
        var starting_location;
        var clicked;
        
        var nodes=[{x:50, y:50, name:array_of_winners[0]['Author'], color: global_color_index}];
        var links=[];
        var force=d3.layout.force()
                .size([500,500])
                .links(links)
                .nodes(nodes)
                .gravity(.5)
                .linkDistance(40)
                .charge(-500)
                .on("tick" , tick);
        var link=canvas.selectAll(".link").data(links)
        var node=canvas.selectAll(".node").data(nodes)
        node.enter()
            .append("circle")
            .attr("r", "5")
            .attr("fill", function(d){return color(d.color)})
            .attr("class", "node")
            .on("mousedown", function(d){mousedown(d.name)})
            .call(force.drag);
        
        node.append("title")
            .text(function(d){return d.name});
        node.exit().remove();
        
        link.enter()
        .insert("line", ".node")
        .attr("class", "line")
        .attr("stroke", "#000000")
        link.exit().remove();
        //returns only list of new nodes
        function checkConnections(data, name, nodes){
            for(var a=0; a<data.length; a+=1)if(data[a]["Author"]==name)new_list=nodes.concat(nodeMakeFromList(data[a]["Co-Authors"]));
            return new_list;
        }
        
        
        var keyDidPress=0;
        function mousedown(name){
            if(keyDidPress==0){
            global_color_index+=1;
            //step 0
            var mothernode;
            for(var a=0; a<nodes.length; a++){
                if (nodes[a].name==name)mothernode=a;
            }
            var length_of_array=nodes.length
            //step 1 
            new_nodes=checkConnections(data, name, nodes)
            for(var a=0; a<nodes.length; a++){
                for(var b=0; b<new_nodes.length; b++){
                    if(nodes[a].name===new_nodes[b].name){
                        if(nodes[a].color!=nodes[mothernode].color){
                        links.push(linkMake(a,mothernode))
                        }
                        new_nodes.splice(b, 1);
                        b--;
                    }
                }
            }
            

            //step 2
            for (var a=0; a<new_nodes.length; a+=1)
            {
                nodes.push(nodeMake(new_nodes[a].name))
            }
            for (var a=length_of_array; a<nodes.length; a+=1){
                links.push(linkMake(mothernode, a))
            }
            
            //find all co-author nodes
            //sending links because checkConnections only returns full node dataset
            
            //updateLinks
            link=canvas.selectAll(".link").data(links);
            link.enter().insert("line", ".node")
            .attr("class", "link")
            .attr("stroke", "#000000");
            link.exit().remove();
            //update nodes
            node=canvas.selectAll(".node").data(nodes);
            node.enter()
                .append("circle")
                .attr("r", 5)
                .attr("fill", function(d){return color(d.color)})
                .attr("class", "node")
                .on("mousedown", function(d){mousedown(d.name)})
                .call(force.drag);
            node.append("title")
                .text(function(d){return d.name});
            node.exit().remove();
            

            //restart force graph
            force.start();
            
            }
        }
        function tick(){
            link.attr("x1", function(d){return d.source.x})
            .attr("x2", function(d){return d.target.x})
            .attr("y1", function(d){return d.source.y})
            .attr("y2", function(d){return d.target.y})
            
            node.attr("cx", function(d){return d.x})
                .attr("cy", function(d){return d.y})

        };
        force.start()
     }
    d3.json("authordata.json", function(data){
            array_of_winners=updateTable(data);
            updateGraph(data,array_of_winners);
            visualizeData(array_of_winners);
    })
    </script>
    </body>
</html>
