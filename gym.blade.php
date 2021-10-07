@extends('layouts.app')

@section('style')
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/css/bootstrap.min.css" rel="stylesheet">  
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css">
@endsection

@section('content') 



<div  id="app" >
    <div class="mx-auto col-5" style="margin-top: 5rem;">

        <form v-on:submit="getData">

            <div id="eroro" class="alert alert-danger" role="alert" style="display : none ;">

            </div>  
            <input type="text" v-model="date" class="form-control"  id="timesport" placeholder="Choisir l'heure de sport" required>
            <button type="submit"  class="btn btn-info" style="margin-top: 1rem;" :disabled="!found"  > Ajouter </button>

        </form>


    </div>


    <div>


    </div>

    <p>
        {% reservations %}
    </p>

</div>


@endsection



@section('javascript') 

<!-- <script src="https://cdn.jsdelivr.net/npm/vue@2.6.12/dist/vue.js"></script> -->
<script src="https://cdn.jsdelivr.net/npm/vue@2.6.0"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/js/bootstrap.bundle.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/flatpickr"></script>
<script src="https://cdn.jsdelivr.net/npm/axios@0.12.0/dist/axios.min.js"></script>
<script >

const id = "{{ json_encode(Auth::user()->id) }}"
const sex = "{{ json_encode(Auth::user()->gender) }}"

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
            date: '',
            reservations :[]

        }
    },



    created () {

        setInterval(() => {
            axios
            .get('/reservations')
            .then(response => (this.reservations = response.data))
            console.log("created")
        }, 1000);

    },

    methods : {
        getData(event) {
            event.preventDefault()
            reservation = this.date.toString().substr(0,14)+"00:00"
            console.log(reservation)
            axios.post('/reservations',{'user_id':id ,'reservation_time' : reservation }).then(response => (console.log(response)))
        }
    },

    computed :{
        found :  function() {
            var v = true
            var allreservations = Array.from(JSON.parse(JSON.stringify(this.reservations)))
            var id_hours =[]
            var full_hours=[]

            count_unique_reservations = allreservations.reduce( (acc, o) => (acc[o.reservation_time] = (acc[o.reservation_time] || 0)+1, acc), {} )
            
            console.log("all reservation")
            console.log(allreservations)
            
            console.log("reservations distinct ")
            console.log( count_unique_reservations)
            for (let item in count_unique_reservations) {
            if (count_unique_reservations[item] >= 5){
                full_hours.push(item)
            }
            }

            console.log("full hours ")
            console.log( full_hours)

            id_reservations =  allreservations.filter( item => item["user_id"] == id,[]);
            console.log( "user reservations" )
            console.log( id_reservations )
            id_reservations.sort((a,b)=>new Date(a["reservation_time"]).getTime()- new Date(b["reservation_time"]).getTime());

            console.log("last three reservations")
            id_reservations_days = id_reservations.map( a => (new Date(a["reservation_time"].substr(0,11))),[]);
            l = id_reservations.length
            last_three_dates = id_reservations.slice(l-3)
            console.log(last_three_dates)


            v1=v2=v3 = true
            message_error = ''


            // first condition 
            if(full_hours.includes(this.date)) {
                message_error = "desole salle est plein , veuillez choisir une autre heure"    
                console.log(1)
                v1=false           
            }

            // second condition
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
                    if (isDateWeek(new Date(id_reservations[item]["reservation_time"]),firstDayOfWeek ,  lastDayOfWeek )){
                        i=i+1
                        console.log(i)
                    }
                }
            }}
            catch(error){
                console.error(error);
            }
            if (i==3 && message_error == '') {
                message_error = "vous avez le droit de 3 seances par semaine , veuillez attendre la semaine prochaine ," +  message_error 
                v2=false
                console.log(2)

            }

            //  third condition
            i=0
            var date_temp = new Date(this.date.toString().substr(0,11))
            for (let dat in id_reservations_days) {
            if (sameDay(id_reservations_days[dat],date_temp ) == 0 && message_error == '') {
                message_error = " vous avez le droit d'une seance par jour , " + message_error 
                console.log(3)
                v3=false
                
            }
            }
            
            // result
            v = v1 && v2 && v3
            if (v) { document.getElementById("eroro").style.display = "none" } else {
                document.getElementById("eroro").style.display = "block"
                document.getElementById("eroro").innerHTML = message_error
            }
            return v

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

@endsection

