<template>
  <div class="greetings">
    <div class="jumbotron">
      <h1 class="display-4"><span class="green">输入要预测的日期</span></h1>
      <p class="lead">Display the forecast data generated by the existing data and algorithm model.</p>
    </div>
  </div>
  <div>
      <div class="container text-center">
        <div class="row align-items-start">
      <div class="col">
      </div>
      <div class="col">
        <div class="input-group">
          <span class="input-group-text">日期格式为形如“01-01”</span>
          <input type="text" id="date-input" v-model="inputDate" />
        </div>
      </div>
      <div class="col">
      </div>
    </div>
  </div>

    <div v-if="selectedData">
     
      <div class="container text-center">
        <div class="row">
          <div class="col order-first">
            <label for="range-selector">预测范围:</label>
            <select id="range-selector" v-model="selectedRange">
              <option value="0"><p class="lead">1小时</p></option>
              <option value="1"><p class="lead">1天</p></option>
              <option value="30"><p class="lead">1月</p></option>
              <option value="365"><p class="lead">1年</p></option>
            </select>
          </div>
          <div class="col">
            <label for="additional-option">选择集群:</label>
            <select id="additional-option" v-model="selectedOption">
              <option value="1">集群1</option>
              <option value="2">集群2</option>
              <option value="3">集群3</option>
            </select>
          </div>
          <div class="col order-last">
            <button @click="fetchData">点击此处查看结果</button>
          </div>
    </div>
  </div>
      <table class="table">
        <thead class="table-dark">
  <tr>
    <th scope="col">日期</th>
    <th scope="col">数值</th>
    <th scope="col">告警</th>
  </tr>
</thead>
<tbody class="table-group-divider">
  <tr v-for="(data, index) in responseData" :key="index">
    <td>{{ dateArray[index] }}</td>
    <td>{{ valueArray[index] }}</td>
    <td>{{ warnArray[index] }}</td>
  </tr>
</tbody>
</table>
    </div>
    
      <div class="echart" id="mychart" :style="myChartStyle"></div>
    
  </div>
</template>

<script>
import axios from "axios";
import * as echarts from "echarts";

export default {
  name: "HelloWorld",
  
  data() {
    return {
      inputDate: "",
      selectedData: null,
      selectedRange: 1,
      selectedOption: 1,
      responseData: [],
      dateArray: [],
      valueArray: [],
      warnArray: [],
      myChart: {},
      myChartStyle: { float: "left", width: "100%", height: "400px" }
    };
  },
  methods: {
    fetchData() {
      const formattedDate = this.formatDate(this.inputDate);
      const apiUrl = `http://127.0.0.1:8000/api/forecast/${formattedDate}/${this.selectedRange}/${this.selectedOption}`;

      axios
        .post(apiUrl, { date: formattedDate, range_value: this.selectedRange, cluster:this.selectedOption })
        .then((response) => {
          const { dateArray, valueArray, warnArray} = response.data; // 假设响应中返回了dateArray和valueArray

          this.dateArray = dateArray;
          this.valueArray = valueArray;
          this.warnArray = warnArray;

          this.responseData = dateArray.map((date, index) => ({
            date: date,
            value: valueArray[index],
            warn: warnArray[index],
            
          }));
          this.initEcharts();

          console.log(response.data);
          console.log("fetchData called");
          console.log(apiUrl);
          console.log(formattedDate);
          console.log(this.selectedRange);
        })
        .catch((error) => {
          console.error(error);
        });
    },
    formatDate(dateString) {
      const parts = dateString.split("-");
      const month = parts[0].padStart(2, "0");
      const day = parts[1].padStart(2, "0");
      
      return `${month}-${day}`;
    },
    initEcharts() {
      const option = {
        xAxis: {
          data: this.dateArray
        },
        legend: {
          data: ["value"],
          bottom: "0%"
        },
        yAxis: {},
        animation: true,
        animationDuration: 20000,
        series: [
          {
            name: "value",
            data: this.valueArray,
            type: "line",
            smooth: true,
            label: {
              show: true,
              position: "top",
              textStyle: {
                fontSize: 16
              }
            }
          },
         
          
        ]
      };
      this.myChart = echarts.init(document.getElementById("mychart"));
      this.myChart.setOption(option);
      //随着屏幕大小调节图表
      window.addEventListener("resize", () => {
        this.myChart.resize();
      });
    }
      
  },
  watch: {
    inputDate(newDate) {
      this.selectedData = {
        date: newDate,
        value: "",
      };
    },
    
  },
  
};
</script>




