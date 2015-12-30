<html>
<head>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
 <script type="text/javascript" src="http://d3js.org/d3.v2.min.js"></script>

</head>
<body>
<?PHP
    echo $_REQUEST['name'];
    ?>
    <script>
setTimeout(function(){}
    d3.json("authorProfile.json", function(){
            $(document).ready(function(){
                              $("body").append("made it!!!")
                              
                              
                              
                              })
            
            
    })

    </script>
</body>
</html>