
document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');
    var initialLocaleCode = 'en';
    var localeSelectorEl = document.getElementById('locale-selector');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        plugins: ['dayGrid', 'timeGrid', 'list', 'interaction'], // an array of strings!
        defaultView: 'dayGridMonth',
        selectable: true,
        selectMirror: true,
        locale: 'pt-br',
        select: function (arg) {
            var title = prompt('Adicionar Tarefa:');
            if (title) {
                calendar.addEvent({
                    title: title,
                    start: arg.start,
                    end: arg.end,
                    allDay: arg.allDay
                })
            }
            calendar.unselect()
        },
        editable: true, //Permite editar as tarefas 
        eventLimit: true, // permitir "mais" link quando muitos eventos
    });
    calendar.render();
});