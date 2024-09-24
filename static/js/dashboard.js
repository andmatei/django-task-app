const csrfToken = $('meta[name="csrf-token"]').attr('content');

const dateRange = (startDate, endDate) => {
    const dates = [];
    let currentDate = new Date(startDate);
    const end = new Date(endDate);

    while (currentDate <= end) {
        dates.push(new Date(currentDate));
        currentDate.setDate(currentDate.getDate() + 1);
    }

    return dates;
}
let stats, startDate, endDate;

async function getData(){
    try {
        const response = await $.getJSON("/api/tasks");

        stats = await response.stats;
        startDate = await response.start_date;
        endDate = await response.end_date;
        console.log(response);
        return response

    } catch (error) {
      console.error(error);
      return error
    }
}

getData().then(response => {
    console.log("hallo :3")
    // const stats = JSON.parse(document.getElementById("stats").textContent);
    // const startDate = JSON.parse(document.getElementById("start_date").textContent);
    // const endDate = JSON.parse(document.getElementById("end_date").textContent);

    const dateStats = stats.dates;
    const countStats = stats.counts;

    print

    const dates = dateRange(startDate, endDate);

    const PRIORITY = {
        HIGH: {
            field: "high_priority",
            name: "High Priority",
        },
        MEDIUM: {
            field: "medium_priority",
            name: "Medium Priority",
        },
        LOW: {
            field: "low_priority",
            name: "Low Priority",
        },
    }


    const getPieCharOptions = () => {
        return {
            series: [
                countStats[PRIORITY.HIGH.field],
                countStats[PRIORITY.MEDIUM.field],
                countStats[PRIORITY.LOW.field]
            ],
            colors: ["#F05252", "#fdba74", "#60a5fa"],
            chart: {
                height: 420,
                type: "pie",
            },
            stroke: {
                colors: ["white"],
                lineCap: "",
            },
            plotOptions: {
                pie: {
                    labels: {
                        show: true,
                    },
                    size: "100%",
                    dataLabels: {
                        offset: -25
                    }
                },
            },
            labels: [PRIORITY.HIGH.name, PRIORITY.MEDIUM.name, PRIORITY.LOW.name],
            dataLabels: {
                enabled: true,
                style: {
                    fontFamily: "Inter, sans-serif",
                },
            },
            legend: {
                position: "bottom",
                fontFamily: "Inter, sans-serif",
            },
            yaxis: {
                labels: {
                    formatter: function (value) {
                        return value + "%"
                    },
                },
            },
            xaxis: {
                labels: {
                    formatter: function (value) {
                        return value + "%"
                    },
                },
                axisTicks: {
                    show: false,
                },
                axisBorder: {
                    show: false,
                },
            },
        }
    }



    const getLineChartOptions = () => {
        return {
            chart: {
                height: "180",
                maxWidth: "100%",
                type: "area",
                fontFamily: "Inter, sans-serif",
                dropShadow: {
                    enabled: false,
                },
                toolbar: {
                    show: false,
                },
            },
            tooltip: {
                enabled: true,
                x: {
                    show: false,
                },
            },
            fill: {
                type: "gradient",
                gradient: {
                    opacityFrom: 0.55,
                    opacityTo: 0,
                    shade: "#1C64F2",
                    gradientToColors: ["#1C64F2"],
                },
            },
            dataLabels: {
                enabled: false,
            },
            stroke: {
                width: 6,
            },
            grid: {
                show: true,
                strokeDashArray: 4,
                padding: {
                    left: 2,
                    right: 2,
                    top: 0
                },
            },
            series: [
                {
                    name: "Tasks",
                    data: dateStats.total,
                    color: "#1A56DB",
                },
            ],
            xaxis: {
                categories: dates.map(date => date.toDateString()),
                labels: {
                    show: false,
                },
                axisBorder: {
                    show: true,
                },
                axisTicks: {
                    show: true,
                },
            },
            yaxis: {
                show: false,
            },
        }
    }


    const getBarChartOptions = () => {
        return {
            colors: ["#1A56DB", "#FDBA8C", "#FDBA8C"],
            series: [
                {
                    name: "Low Priority",
                    color: "#1A56DB",
                    data: dates.map((date, index) => ({ x: date.toDateString(), y: dateStats[PRIORITY.LOW.field][index] })),
                },
                {
                    name: "Medium Priority",
                    color: "#FDBA8C",
                    data: dates.map((date, index) => ({ x: date.toDateString(), y: dateStats[PRIORITY.MEDIUM.field][index] })),
                },
                {
                    name: "High Priority",
                    color: "#FDBA8C",
                    data: dates.map((date, index) => ({ x: date.toDateString(), y: dateStats[PRIORITY.HIGH.field][index] })),
                },
            ],
            chart: {
                type: "bar",
                height: "320px",
                width: "100%",
                fontFamily: "Inter, sans-serif",
                toolbar: {
                    show: false,
                },
            },
            plotOptions: {
                bar: {
                    horizontal: false,
                    columnWidth: "70%",
                    borderRadiusApplication: "end",
                    borderRadius: 8,
                },
            },
            tooltip: {
                shared: true,
                intersect: false,
                style: {
                    fontFamily: "Inter, sans-serif",
                },
            },
            states: {
                hover: {
                    filter: {
                        type: "darken",
                        value: 1,
                    },
                },
            },
            stroke: {
                show: true,
                width: 0,
                colors: ["transparent"],
            },
            grid: {
                show: true,
                strokeDashArray: 4,
                padding: {
                    left: 2,
                    right: 2,
                    top: -14
                },
            },
            dataLabels: {
                enabled: false,
            },
            legend: {
                show: true,
            },
            xaxis: {
                floating: false,
                labels: {
                    show: false,
                    style: {
                        fontFamily: "Inter, sans-serif",
                        cssClass: 'text-xs font-normal fill-gray-500 dark:fill-gray-400'
                    }
                },
                axisBorder: {
                    show: false,
                },
                axisTicks: {
                    show: false,
                },
            },
            yaxis: {
                show: false,
            },
            fill: {
                opacity: 1,
            },
        }
    }



    if (document.getElementById("line-chart") && typeof ApexCharts !== 'undefined') {
        const chart = new ApexCharts(document.getElementById("line-chart"), getLineChartOptions());
        chart.render();
    }


    if (document.getElementById("pie-chart") && typeof ApexCharts !== 'undefined') {
        const chart = new ApexCharts(document.getElementById("pie-chart"), getPieCharOptions());
        chart.render();
    }

    console.log(document.getElementById("column-chart"));

    if (document.getElementById("column-chart") && typeof ApexCharts !== 'undefined') {
        const chart = new ApexCharts(document.getElementById("column-chart"), getBarChartOptions());
        chart.render();
    }

    document.getElementById("total-tasks-urgent").innerHTML = countStats.urgent || 0;
    document.getElementById("total-tasks").innerHTML = countStats.total || 0;

    const tasks = response.page.tasks; // Adjust based on your API response structure
    const tableBody = $('#task-table-body');
    tableBody.empty();
    tasks.forEach((task, index) => {
        tableBody.append(createTaskRow(task, index));
    });


})










function createPriorityBadge(priority) {
    let badgeClass = '';
    let badgeText = '';

    switch (priority) {
        case 1:
            badgeClass = 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300';
            badgeText = 'Low';
            break;
        case 2:
            badgeClass = 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300';
            badgeText = 'Medium';
            break;
        case 3:
            badgeClass = 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300';
            badgeText = 'High';
            break;
    }

    return `<span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded ${badgeClass}">${badgeText}</span>`;
}

function createTaskRow(task, index) {
    return `
        <tr class="bg-white border-b">
            <th scope="row" class="px-6 py-3 font-medium text-gray-900 whitespace-nowrap">
                ${task.task}
            </th>
            <td class="px-6 py-3">
                ${task.user_email}
            </td>
            <td class="px-6 py-3">
                ${task.due_by}
            </td>
            <td class="px-6 py-3">
                ${createPriorityBadge(task.priority)}
            </td>
            <td class="px-6 py-3">
                <input type="checkbox" ${task.is_urgent ? 'checked' : ''} disabled
                    class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
            </td>
            <td class="px-6 py-3">
                <div class="flex items-center">
                    <button id="widgetDropdownButton-${index}"
                        data-dropdown-toggle="widgetDropdown-${index}" data-dropdown-placement="bottom"
                        type="button"
                        class="inline-flex items-center justify-center text-gray-500 w-8 h-8 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-700 rounded-lg text-sm">
                        <svg class="w-3.5 h-3.5 text-gray-800 dark:text-white" aria-hidden="true"
                            xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 16 3">
                            <path d="M2 0a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3Zm6.041 0a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM14 0a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3Z" />
                        </svg><span class="sr-only">Open dropdown</span>
                    </button>
                    <div id="widgetDropdown-${index}"
                        class="z-20 hidden bg-white divide-y divide-gray-100 rounded-lg shadow w-44 dark:bg-gray-700">
                        <ul class="py-2 text-sm text-gray-700 dark:text-gray-200"
                            aria-labelledby="widgetDropdownButton-${index}">
                            <li>
                                <a href="/tasks/${task.id}/edit/"
                                    class="flex w-full items-center px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">
                                    <svg class="w-3 h-3 me-2" aria-hidden="true"
                                        xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 21 21">
                                        <path stroke="currentColor" stroke-linecap="round"
                                            stroke-linejoin="round" stroke-width="2"
                                            d="M7.418 17.861 1 20l2.139-6.418m4.279 4.279 10.7-10.7a3.027 3.027 0 0 0-2.14-5.165c-.802 0-1.571.319-2.139.886l-10.7 10.7m4.279 4.279-4.279-4.279m2.139 2.14 7.844-7.844m-1.426-2.853 4.279 4.279" />
                                    </svg>Edit
                                </a>
                            </li>
                            <li>
                                <form action="/api/tasks/${task.id}" onsubmit="deleteTask(event)">
                                    <button type="submit"
                                        class="flex items-center w-full px-4 py-2 text-red-600 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">
                                        <svg class="w-3 h-3 me-2" aria-hidden="true"
                                            xmlns="http://www.w3.org/2000/svg" fill="currentColor"
                                            viewBox="0 0 20 20">
                                            <path d="M14.707 7.793a1 1 0 0 0-1.414 0L11 10.086V1.5a1 1 0 0 0-2 0v8.586L6.707 7.793a1 1 0 1 0-1.414 1.414l4 4a1 1 0 0 0 1.416 0l4-4a1 1 0 0 0-.002-1.414Z" />
                                            <path d="M18 12h-2.55l-2.975 2.975a3.5 3.5 0 0 1-4.95 0L4.55 12H2a2 2 0 0 0-2 2v4a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-4a2 2 0 0 0-2-2Zm-3 5a1 1 0 1 1 0-2 1 1 0 0 1 0 2Z" />
                                        </svg>Delete
                                    </button>
                                </form>
                            </li>
                        </ul>
                    </div>
                </div>
            </td>
        </tr>
    `;
}

function deleteTask(event) {
    event.preventDefault();
    const url = $(event.target).closest('form').attr('action');
    console.debug(`Deleting task at url: ${url}`);
    
    const id = $(event.target).parents('form').attr('data-task-id');
    $.ajax({
        url: url,
        type: 'DELETE',
        headers: {
            'X-CSRFToken':csrfToken 
        },
        data: { id: id },
        success: function (data) {
            window.location.reload();
        }
    });
}
