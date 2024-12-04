<template>
	<div class="flex flex-col w-max-screen-lg mx-[15vw]">
		<div class="flex my-5 gap-5">
			<div class="card bg-base-100 shadow-xl flex-1">
				<h1 class="card-title text-center mx-auto">Éves bevétel</h1>
				<div class="card-body">
					<p class="flex flex-col items-center">
						<span class="font-bold">Nettó</span>
						<span> {{ formatNumber(annual_sales) }} Ft</span>
					</p>
					<p class="flex flex-col items-center">
						<span class="font-bold">Bruttó</span>
						<span>{{ formatNumber(annual_sales * 1.27) }} Ft</span>
					</p>
				</div>
			</div>
			<div class="card bg-base-100 shadow-xl flex-1">
				<h1 class="card-title text-center mx-auto">Havi bevétel</h1>
				<div class="card-body">
					<p class="flex flex-col items-center">
						<span class="font-bold">Nettó</span>
						<span>{{ formatNumber(monthly_sales.length > 0 ? monthly_sales[monthly_sales.length - 1] : 0) }}
							Ft</span>
					</p>
					<p class="flex flex-col items-center">
						<span class="font-bold">Bruttó</span>
						<span>{{ formatNumber(monthly_sales.length > 0 ? monthly_sales[monthly_sales.length - 1] * 1.27 : 0) }} Ft</span>
					</p>
				</div>
			</div>
			<div class="card bg-base-100 shadow-xl flex-1">
				<h1 class="card-title text-center mx-auto">Legnagyobb értékű számlák</h1>
				<div class="card-body">
					<p class="font-bold text-center text-lg">{{ most_revenued_partner }}</p>
				</div>
			</div>
			<div class="card bg-base-100 shadow-xl flex-1">
				<h1 class="card-title text-center mx-auto">Legtöbb számla kiállítva</h1>
				<div class="card-body">
					<p class="font-bold text-center text-lg">{{ most_bills_customer }}</p>
				</div>
			</div>
		</div>
	</div>
	<div class="chart-container">
		<canvas id="monthly-sales-chart"></canvas>
	</div>
</template>

<script>
import axios from "axios";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables); // Register chart.js components

export default {
	data() {
		return {
			monthly_sales: [], // Monthly net sales data
			gross_sales: [], // Monthly gross sales data (net * 1.27)
			annual_sales: 0, // Total annual sales
			most_revenued_partner: "", // Placeholder for partner with the highest sales
			most_bills_customer: "",
			chart: null, // Chart.js instance
		};
	},
	methods: {
		getStatistics() {
			const path = "http://localhost:5000/getStatistics";
			axios
				.get(path)
				.then((res) => {
					const sales_data = res.data.monthly_sales;					
					const labels = this.generateLabels();
					const aligned_sales = this.alignSalesDataWithLabels(labels, sales_data);
					this.monthly_sales = aligned_sales;
					this.gross_sales = aligned_sales.map((net) => (net * 1.27).toFixed(2));
					this.annual_sales = res.data.annual_sales;
					this.most_revenued_partner = res.data.highest_customer.name;
					this.most_bills_customer = res.data.most_bills_customer.name;
					this.createChart();
				})
				.catch((error) => {
					console.error(error);
				});
		},
		formatNumber(value) {
			return new Intl.NumberFormat('hu-HU', {
				style: 'decimal',
				useGrouping: true,
				maximumFractionDigits: 0
			}).format(value);
		},
		createChart() {
			if (this.monthly_sales.length === 0) return;

			if (this.chart) {
				this.chart.destroy();
			}

			const ctx = document.getElementById("monthly-sales-chart").getContext("2d");

			this.chart = new Chart(ctx, {
				type: "bar",
				data: {
					labels: this.generateLabels(),
					datasets: [
						{
							label: "Nettó",data: this.monthly_sales,
							backgroundColor: "rgba(75, 192, 192, 0.6)",
							borderColor: "rgba(75, 192, 192, 1)",
							borderWidth: 1,
							barPercentage: 0.9,
							categoryPercentage: 0.8,
						},
						{
							label: "Bruttó",
							data: this.gross_sales,
							backgroundColor: "rgba(153, 102, 255, 0.6)",
							borderColor: "rgba(153, 102, 255, 1)",
							borderWidth: 1,
							barPercentage: 0.9,
							categoryPercentage: 0.8,
						},
					],
				},
				options: {
					responsive: true,
					maintainAspectRatio: false,
					scales: {
						y: {
							beginAtZero: true,
							ticks: {
								callback: function (value) {
									return value + " Ft";
								},
							},
						},
					},
				},
			});
		},
		generateLabels() {
			const currentDate = new Date();
			const labels = [];
			for (let i = 11; i >= 0; i--) {
				const labelDate = new Date(currentDate.getFullYear(), currentDate.getMonth() - i, 1);
				const label = labelDate.toLocaleString("default", { month: "long", year: "numeric" });
				labels.push(label);
			}
			return labels;
		},
		alignSalesDataWithLabels(labels, sales_data) {
			const salesMap = {};

			labels.forEach((label) => {
				salesMap[label] = 0;
			});

			for (const [month_year, total_sales] of Object.entries(sales_data)) {
				const label = new Date(`${month_year}.01`).toLocaleString("default", {
					month: "long",
					year: "numeric",
				});

				if (salesMap.hasOwnProperty(label)) {
					salesMap[label] = total_sales;
				}
			}

			// Return sales data aligned with labels
			return Object.values(salesMap);
		},
	},
	mounted() {
		this.getStatistics(); // Fetch statistics when the component is mounted
	},
};
</script>

<style scoped>
.chart-container {
	max-width: 800px;
	margin: 0 auto;
	position: relative;
	height: 400px;
	/* Adjust height as needed */
}

canvas {
	width: 100% !important;
	/* Ensure the chart takes full width */
	height: 100% !important;
	/* Ensure the chart takes full height */
}
</style>