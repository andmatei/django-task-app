


// $.getJSON("/api/stats", function(data) {
//     stats = data.stats;
//     startDate = data.start_date;
//     endDate = data.end_date;    
// })



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
      stats = response.stats;
      startDate = response.start_date;
      endDate = response.end_date;
      console.log(response);

    } catch (error) {
      console.error(error);
    }
    console.log("MAAA PWEASEE :C")
}

getData()

console.log(stats)
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
