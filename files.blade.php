
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <title>Document</title>
</head>
<body>

    <div class="container">


        @foreach( $filenames as $file )
  

             
            <div class="card" style="margin:3rem;   text-align: center;">
            <a href="uploads/{{ $file }}" style="  font-style: none;">  
            <img class="card-img-top  image_file" src="uploads/{{ $file }}" alt="file image">
            <div class="card-body" >
                <h2 class="card-text  titre_file">{{ $file }}</h2>
            </div>
            </a>
            </div>

            <!-- condition pdf -->
                        <!-- Embed PDF File -->
                        <!-- <object data="YourFile.pdf" type="application/x-pdf" title="SamplePdf" width="500" height="720">
                            <a href="YourFile.pdf">shree</a> 
                        </object> -->
            


        @endforeach

    </div>
    <!-- for -->
            <!-- <img src="uploads/{{ Session::get('filenames') }}"> -->

</body>
</html>