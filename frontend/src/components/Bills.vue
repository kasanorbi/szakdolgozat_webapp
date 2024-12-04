<template>
    <div class="flex flex-col w-max-screen-lg mx-[15vw]">
        <h1 class="w-full text-center text-7xl mt-[3vh] font-extrabold">Számlák</h1>

        <div class="flex flex-col space-y-4 mt-4">
            <details v-for="bill in bills" :key="bill.bill_id" class="collapse collapse-arrow bg-base-200">
                <summary class="collapse-title text-xl font-medium">
                    {{ formatBillSummary(bill) }}
                </summary>
                <div class="collapse-content">
                    <div class="w-full flex flex-col">
                        <p>{{ bill.customer_details.customer_name }}</p>
                        <p>{{ bill.customer_details.postal_code }}</p>
                        <p>{{ bill.customer_details.settlement }}, {{ bill.customer_details.address }}</p>
                        <p>Adószám: {{ bill.customer_details.tax_number }}</p>
                    </div>
                    <p>
                        <strong class="-mb-3">Tételek</strong>
                    <ul>
                        <li v-for="item in bill.items" :key="item.item_id">
                            {{ item.name }} - {{ item.amount }} db - {{ item.price.toFixed(2) * 1.27 }} Ft
                        </li>
                    </ul>
                    </p>
                    <div class="w-full flex flex-col items-end">
                        <p><strong>Összesen Nettó:</strong> {{ calculateNetTotal(bill.items).toFixed(2) }} Ft</p>
                        <p><strong>Összesen Bruttó:</strong> {{ calculateGrossTotal(bill.items).toFixed(2) }} Ft</p>
                    </div>
                </div>
            </details>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            bills: [],
        };
    },
    methods: {
        async fetchBillData() {
            try {
                const response = await axios.get('http://localhost:5000/getBillData');
                this.bills = response.data;
            } catch (error) {
                console.error("Error fetching bill data:", error);
            }
        },
        formatBillSummary(bill) {
            const billId = `KC-${String(bill.bill_id).padStart(4, '0')}`;
            return `${billId} ${bill.customer_details.customer_name} - ${bill.date}`;
        },
        calculateNetTotal(items) {
            return items.reduce((total, item) => total + (item.price * item.amount), 0);
        },
        calculateGrossTotal(items) {
            return this.calculateNetTotal(items) * 1.27;
        },
    },
    mounted() {
        this.fetchBillData();
    },
};
</script>

<style scoped>
.collapse {
    cursor: pointer;
}

.collapse-content {
    padding: 10px;
    border-top: 1px solid #ccc;
}
</style>
