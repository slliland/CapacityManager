<template>
  <div class="echart" id="mychart" :style="myChartStyle"></div>
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
      myChartStyle: { float: "left", width: "100%", height: "400px" } //图表样式
    };
  },
  mounted() {
    axios.get("../../3_2_predictions.json").then(response => {
      this.xData = response.data.xData;
      this.y1Data = response.data.y1Data;
      this.y2Data = response.data.y2Data;
      this.y3Data = response.data.y3Data;
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
