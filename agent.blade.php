<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta date="viewport" content="width=device-width, initial-scale=1.0">
    <!-- CSS only -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/css/bootstrap.min.css" rel="stylesheet">  
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css">
    <script src="https://cdn.jsdelivr.net/npm/vue@2.6.12/dist/vue.js"></script>


    <title>MyOplaGym</title>
</head>
<body >

<div  id="app" >
    <div class="mx-auto col-5" style="margin-top: 5rem;">

        <form v-on:submit="getDate">

            <p style="color:red;">{% found %}</p>
            <input type="text" v-model="date" class="form-control"  id="timesport" placeholder="Choisir l'heure de sport" required>
            <button type="submit"  class="btn btn-info" style="margin-top: 1rem;" > Ajouter </button>

        </form>


    </div>


    <p>
                {% date %}
    </p>


</div>


    
<!-- CSS only -->
<!-- JavaScript Bundle with Popper -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/js/bootstrap.bundle.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/flatpickr"></script>
<script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
<script >


var user_id = 1
var reserved_date = "2021-09-26 12:00"
var reservations = [

{"id":"1","date":"2021-09-26 13:00"} ,
{"id":"1","date":"2021-09-25 14:00"} ,
{"id":"1","date":"2021-09-22 17:00"} ,
{"id":"1","date":"2021-09-22 18:00"} ,
{"id":"1","date":"2021-09-22 12:00"} ,
{"id":"1","date":"2021-09-22 14:00"} ,
{"id":"1","date":"2021-09-21 13:00"} ,
{"id":"1","date":"2021-09-23 14:00"} ,
{"id":"1","date":"2021-09-23 14:00"} ,
{"id":"1","date":"2021-09-22 14:00"} ,
{"id":"1","date":"2021-09-22 14:00"} ,
{"id":"1","date":"2021-09-22 14:00"} ,
{"id":"1","date":"2021-09-22 14:00"} ,
{"id":"1","date":"2021-09-22 14:00"} ,

]

var full_hours =[]
var id_hours =[]
var count_unique_reservations =  reservations.reduce( (acc, o) => (acc[o.date] = (acc[o.date] || 0)+1, acc), {} )

for (let item in count_unique_reservations) {
   if (count_unique_reservations[item] >= 5){
       full_hours.push(item)
   }
}

var id_reservations =  reservations.filter( item => item["id"] == user_id,[]);
id_reservations.sort((a,b)=>new Date(a["date"]).getTime()- new Date(b["date"]).getTime());
id_reservations_days = id_reservations.map( a => (new Date(a.date.toString().substr(0,11))),[]);
l = id_reservations.length
last_three_dates = id_reservations.slice(l-3)
console.log(last_three_dates)

// code of same week
function weeksBetween(d1, d2) {
    return Math.round(Math.abs(d2 - d1) / (7 * 24 * 60 * 60 * 1000))
}

function sameDay(d1,d2){
    return Math.ceil(Math.abs(d2 - d1) / (7 * 24 * 60 * 60 * 1000))
}


function isDateWeek(date1,firstDayOfWeek ,lastDayOfWeek) {
  // if date is equal or within the first and last dates of the week
  return date1 >= firstDayOfWeek && date1 <= lastDayOfWeek;
}

var app = new Vue({
    
    delimiters: ['{%', '%}'],
    
    el: '#app',
    
    data() {
    return {
        id : 1,
        date: '',
        sex:'M',
        resr: full_hours,
    }
    },

    methods:{
        getDate : function(event) {
            event.preventDefault() // it prevent from page reload
            reservation = new Date(this.date.toString().substr(0,14)+"00")
            ids = []
            times = []
            
        }
    },
    
    computed:{
        found : function() {

            if( this.resr.includes(this.date)) {
                return "desole salle est plein , veuillez choisir une autre heure"               
            }

            var i = 0
            try {
            var tObj = new Date(this.date.toString().substr(0,11));
            var tDate = tObj.getDate();
            var tDay = tObj.getDay();

            // get first date of week
            var firstDayOfWeek = new Date(tObj.setDate(Math.abs(tDate - tDay)));

            // get last date of week
            var lastDayOfWeek = new Date(firstDayOfWeek);
            lastDayOfWeek.setDate(lastDayOfWeek.getDate() + 6);

            console.log(lastDayOfWeek  ,firstDayOfWeek  )
            lastDayOfWeek.setDate(lastDayOfWeek.getDate() + 6);
            if (last_three_dates.length == 3){
                for (let item in last_three_dates) {
                    if (isDateWeek(new Date(id_reservations[item]["date"]),firstDayOfWeek ,  lastDayOfWeek )){
                        i=i+1
                        console.log(i)
                    }
                }
            }}
            catch(error){
                console.error(error);
            }
            if (i==3) {
                return "vous avez le droit de 3 seances par semaine , veuillez attendre la semaine prochaine ."
            }
            i=0

            var date_temp = new Date(this.date.toString().substr(0,11))
            for (let dat in id_reservations_days) {
            if (sameDay(id_reservations_days[dat],date_temp) == 0) {
                return "vous avez le droit d'une seance par jour ."
            }
            }
            
        }
    }

  
})

var nTime =""
var MTime = ""
// calender
if (app.$data.sex == "M") {
    mTime= "07:00"
    MTime= "12:00"
}else{
    mTime= "13:00"
    MTime= "18:00"
}

config = {
    time_24hr: true,
    enableTime: true,
    altInput : true ,
    dateFormat: "Y-m-d H:00",
    altFormat:  "Y-m-d H:00",
    minTime: mTime,
    maxTime: MTime,
    minDate: "today",
    maxDate: new Date().fp_incr(6), // 6 days from now
    "locale": {
    "firstDayOfWeek": 1 // start week on Monday
    },
}
fp=flatpickr("#timesport",config)
fp.minuteElement.style.display = 'none'


</script>

</body>
</html>

