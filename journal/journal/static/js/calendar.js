// let stories = async() => {
//   const response = await fetch("api/journey/get_story?format=json");
//   let data = await response.json();
//   console.log(data);
// }

// let data = []
// async function foo() {
//   let obj;
//   const res = await fetch('api/journey/get_story?format=json')
//   obj = await res.json();
//   // console.log(obj)
// }

// async function getValue() {
//   console.log("here");
//   const result = await foo();
//   console.log(result); // Output: Data fetched successfully
//   return result;
// }

// let x = getValue();
// console.log(x);


async function fetchStories() {
  try {
    const response = await fetch('api/journey/get_story?format=json', {
      method: 'GET',
      credentials: 'same-origin'
    });
    const stories = await response.json();
    return stories;
  } catch (error) {
    console.error(error);
  }
}

// function showCalendar(envetData) {
//   document.addEventListener('DOMContentLoaded', function () {
//     var calendarEl = document.getElementById('calendar');
//     console.log(calendarEl);
//     var calendar = new FullCalendar.Calendar(calendarEl, {
//       headerToolbar: {
//         left: 'prev,next today',
//         center: 'title',
//         right: 'dayGridYear,dayGridMonth,timeGridWeek'
//       },
//       initialView: 'dayGridYear',
//       initialDate: '2023-01-12',
//       editable: true,
//       selectable: true,
//       dayMaxEvents: true, // allow "more" link when too many events
//       // businessHours: true,
//       // weekends: false,
//       // events: stories,
//       events: [
//         {
//           title: 'All Day Event',
//           start: '2024-01-01'
//         },
//         {
//           title: 'Long Event Name Name',
//           start: '2024-03-07',
//           end: '2023-01-10'
//         },
//         {
//           groupId: 999,
//           title: 'Repeating Event',
//           start: '2024-02-09T16:00:00'
//         },
//         {
//           groupId: 999,
//           title: 'Repeating Event',
//           start: '2023-01-16T16:00:00'
//         },
//         {
//           title: 'Conference',
//           start: '2023-01-11',
//           end: '2023-01-13'
//         },
//         {
//           title: 'Meeting',
//           start: '2023-01-12T10:30:00',
//           end: '2023-01-12T12:30:00'
//         },
//         {
//           title: 'Lunch',
//           start: '2023-01-12T12:00:00'
//         },
//         {
//           title: 'Meeting',
//           start: '2023-01-12T14:30:00'
//         },
//         {
//           title: 'Happy Hour',
//           start: '2023-01-12T17:30:00'
//         },
//         {
//           title: 'Dinner',
//           start: '2023-01-12T20:00:00'
//         },
//         {
//           title: 'Birthday Party',
//           text: "test",
//           start: '2023-04-29T07:00:00'
//         },
//         {
//           title: 'Click for Google',
//           text: "test",
//           start: '2023-01-28'
//         }
//       ]
//     }
    
//     );

//     calendar.render();
//   });

// }
// }

// showCalendar([]);

async function getStories() {
  const stories = await fetchStories();
  convertedStories = []
  stories.map(story => {
    let entry = {
      title: story.title,
      start: story.date_start,
      end: story.date_end
    }
    convertedStories.push(entry);
  })
  showCalendar(convertedStories)

}

function showCalendar(envetData) {
  var calendarEl = document.getElementById('calendar');
  // console.log(calendarEl);
  // console.log(envetData);
  // document.addEventListener('DOMContentLoaded', function () {
  //   console.log(calendarEl);
    var calendar = new FullCalendar.Calendar(calendarEl, {
      headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: 'dayGridYear,dayGridMonth,timeGridWeek'
      },
      initialView: 'dayGridYear',
      initialDate: '2024-01-12',
      editable: true,
      selectable: true,
      dayMaxEvents: true, // allow "more" link when too many events
      // businessHours: true,
      // weekends: false,
      events: envetData,
      // events: [
      //   {
      //     title: 'All Day Event',
      //     start: '2024-03-01'
      //   }
      // ]
    }
    
    );

    calendar.render();
  // });

}



getStories();
