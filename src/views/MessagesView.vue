<template>
  <div>
    
    <div class="echart" id="mychart" :style="myChartStyle"></div>

    <table class="table">
      <thead>
      <tr>
        <th>日期</th>
        <th>预测上界</th>
        <th>预测值</th>
        <th>预测下界</th>
        <th>是否超出容量</th>
      </tr>
    </thead>
    <tbody class="table-group-divider">
      <tr v-for="(item, index) in tableData" :key="index">
        <td>{{ item.x }}</td>
        <td>{{ item.y1 }}</td>
        <td>{{ item.y2 }}</td>
        <td>{{ item.y3 }}</td>
        <td>{{ item.warn }}</td>
      </tr>
    </tbody>
    </table>
  </div>
</template>

<script>
import * as echarts from "echarts";
import axios from "axios";

export default {
  data() {
    return {
      myChart: {},
      xData: [],
      y1Data: [],
      y2Data: [],
      y3Data: [],
      warnData:[],
      myChartStyle: { float: "left", width: "100%", height: "400px" }, //图表样式
      tableData: [],
    };
  },
  mounted() {
    axios.get("../../3_2_predictions.json").then(response => {
      this.xData = response.data.xData;
      this.y1Data = response.data.y1Data;
      this.y2Data = response.data.y2Data;
      this.y3Data = response.data.y3Data;
      this.warnData = response.data.warn

      // 构造表格数据，将 x、y1、y2、y3 和 warn 数据组合为对象
      this.tableData = this.xData.map((x, index) => ({
        x: x,
        y1: this.y1Data[index],
        y2: this.y2Data[index],
        y3: this.y3Data[index],
        warn: this.warnData[index] // 可根据需要添加适当的列数据
      }));

      this.initEcharts();
    }).catch(error => {
      console.log(error);
    });
  },
  methods: {
    initEcharts() {
      const option = {
        xAxis: {
          data: this.xData
        },
        legend: {
          data: ["上界", "预测值", "下界"],
          bottom: "0%"
        },
        yAxis: {},
        animation: true,
        animationDuration: 20000,
        series: [
          {
            name: "上界",
            data: this.y1Data,
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
          {
            name: "下界",
            data: this.y2Data,
            type: "line",
            smooth: true,
            label: {
              show: true,
              position: "bottom",
              textStyle: {
                fontSize: 16
              }
            }
          },
          {
            name: "预测值",
            data: this.y3Data,
            type: "line",
            smooth: true,
            label: {
              show: true,
              position: "bottom",
              textStyle: {
                fontSize: 16
              }
            }
          }
        ]
      };
      this.myChart = echarts.init(document.getElementById("mychart"));
      this.myChart.setOption(option);
      //随着屏幕大小调节图表
      window.addEventListener("resize", () => {
        this.myChart.resize();
      });
    }
  }
};
</script>

