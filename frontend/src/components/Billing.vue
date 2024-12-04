<template>
	<div class="flex flex-col w-max-screen-lg mx-[15vw]">
		<h1 class="text-5xl text-center font-bold mt-[3vh]">Számla kiállítás</h1>
		<div class="divider" />
		<div class="flex justify-between">
			<div class="flex flex-col">
				<h1 class="text-xl font-bold text-left">Vevő</h1>
				<div>{{ paramName }}</div>
				<div>{{ paramTaxNumber }}</div>
				<div>{{ paramPostalCode }}</div>
				<div>{{ paramSettlement }}</div>
				<div>{{ paramAddress }}</div>
			</div>
			<div class="text-center">
				<h1 class="text-xl font-bold">Adatok</h1>
				<div>Név</div>
				<div>Adószám</div>
				<div>Irányítószám</div>
				<div>Település</div>
				<div>Cím</div>
			</div>
			<div class="flex flex-col [&>div]:text-right">
				<h1 class="text-xl font-bold text-right">Számla kiállító</h1>
				<div>Kása Car Kft.</div>
				<div>**************</div>
				<div>6067</div>
				<div>Tiszaalpár</div>
				<div>Petőfi Sándor utca 72.</div>
			</div>
		</div>
		<div class="mt-[3vh]">
			<h1 class="text-2xl text-center font-bold">Tételek</h1>
			<div class="divider" />
			<div class="overflow-x-auto">
				<table class="table overflow-x-auto no-scrollbar">
					<thead>
						<tr class="[&>th]:text-center [&>th]:text-2xl">
							<th>Cikkszám</th>
							<th>Megnevezés</th>
							<th>Mennyiség</th>
							<th>Nettó</th>
							<th>Áfa</th>
							<th>Bruttó</th>
						</tr>
					</thead>
					<tbody>
						<template v-if="billedParts.length > 0">
							<tr class="[&>td]:text-lg" v-for="(part, index) in billedParts" :key="index">
								<td>{{ part.itemNumber }}</td>
								<td>{{ part.name }}</td>
								<td>{{ part.amount }} db</td>
								<td>{{ part.price }} Ft</td>
								<td>{{ Math.ceil((part.price) * part.amount * 1.27) - (part.price * part.amount) }} Ft
								</td>
								<td>{{ Math.ceil((part.price) * 1.27) * part.amount }} Ft</td>
								<button class="btn btn-error hover:scale-110" @click="deleteRow(part.id)">
									<span class="material-symbols-outlined"> delete </span>
								</button>
							</tr>
						</template>
						<template v-else>
							<tr>
								<td colspan="9" class="text-center" style="font-size: 30px; margin-top:  1rem;">
									Nincs felírt tétel!
								</td>
							</tr>
						</template>
					</tbody>
				</table>
			</div>
		</div>
		<div>
			<div class="divider" />
			<div class="flex items-center w-full justify-between">
				<div class="flex gap-36">
					<span>Nettó: {{ this.sum }} Ft </span>
					<span style="margin-left: 1rem;">Bruttó: {{ this.sumWithTax }} Ft </span>
				</div>
				<div>
					<button type="button" class="btn btn-accent" @click="createBill">
						<span class="material-symbols-outlined">check</span>
						<span> Számla kiállítása</span>
					</button>
				</div>
			</div>
		</div>
		<div class="flex mt-14 gap-2">
			<label class="input input-bordered flex items-center gap-2">
				<input type="text" id="work" class="grow" v-model="addWork" placeholder="Munka">
			</label>
			<label class="input input-bordered flex items-center gap-2 text-right">
				<input type="number" id="price" class="grow" min="0" step="10" placeholder="Munkadíj"
					v-model="workPrice">
			</label>
			<label class="input input-bordered flex items-center gap-2 text-right">
				<input type="number" id="amount" class="grow" min="0" step="1" placeholder="db" v-model="amount">
			</label>
			<button type="button" class="btn btn-primary" @click="addWorkToBill">
				<span class="material-symbols-outlined"> add </span>
			</button>
		</div>

		<div>
			<div class="divider" />
			<h1 class="text-2xl font-bold text-center">Készlet</h1>
			<label class="input input-bordered flex items-center gap-2">
				<input type="text" id="search" class="grow" v-model="searchQuery" placeholder="Keresés">
			</label>
			<div class="overflow-x-auto mt-[3vh] min-h-96">
				<table class="table">
					<thead class="text-2xl text-center">
						<tr>
							<th></th>
							<th class="hover:cursor-pointer">Cikkszám</th>
							<th class="hover:cursor-pointer">Megnevezés</th>
							<th class="hover:cursor-pointer">Mennyiség</th>
							<th class="hover:cursor-pointer">Nettó</th>
							<th>Bruttó</th>
						</tr>
					</thead>
					<tbody>
						<template v-if="displayedParts.length > 0">
							<tr class="[&>td]:text-lg" v-for="(part, index) in displayedParts" :key="index">
								<td></td>
								<td class="text-left">{{ part.itemNumber }}</td>
								<td class="text-left">{{ part.name }}</td>
								<td>{{ part.amount }} db</td>
								<td>{{ Math.ceil(part.price) }} Ft</td>
								<td>{{ Math.ceil(((part.price) * 1.27)) }} Ft</td>
								<td class="flex gap-2">
									<button type="button" class="btn btn-primary hover:scale-110" title="Hozzáadás"
										@click="addPartToBill(part.id)">
										<span class="material-symbols-outlined"> add </span>
									</button>
									<button type="button" class="btn btn-warning hover:scale-110" title="Módosítás"
										@click="toggleUpdatePartModal(part.id, part.amount, part.itemNumber, part.name, part.price)">
										<span class="material-symbols-outlined"> edit </span>
									</button>
								</td>
							</tr>
						</template>
						<template v-else>
							<tr>
								<td colspan="9" class="text-center" style="font-size: 30px; margin-top:  1rem;">Nem
									található ilyen alkatrész.</td>
							</tr>
						</template>
					</tbody>
				</table>
			</div>
		</div>
	</div>
</template>
<script>
import axios from 'axios';
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';
import router from '../router/index.js';
const notify = (type, message) => {
	switch (type) {
		case 'success':
			toast.success(message, {
				theme: 'dark',
				position: toast.POSITION.TOP_RIGHT
			});
			break;
		case 'error':
			toast.error(message, {
				theme: 'dark',
				position: toast.POSITION.TOP_RIGHT
			});
			break;
		default:
			toast.info(message, {
				theme: 'dark',
				position: toast.POSITION.TOP_RIGHT
			});
	}
}
export default {
	props: ['paramId', 'paramName', 'paramTaxNumber', 'paramPostalCode', 'paramSettlement', 'paramAddress',],
	data() {
		return {
			parts: [],
			billedParts: [],
			searchQuery: '',
			addWork: '',
			amount: '',
			workPrice: '',
			workIndex: 1000,
			sum: 0,
			sumWithTax: 0,
		}
	},
	methods: {
		getParts() {
			const path = 'http://localhost:5000/getComponents';
			axios.get(path).then((res) => {
				this.parts = Object.values(res.data.parts);
				this.nextPartIndex = res.data.nextPartIndex;
			}).catch((error) => {
				console.error(error);
			})
		},
		addPartToBill(partId) {
			const path = `http://localhost:5000/getComponentById/${partId}`;
			axios.get(path)
				.then((res) => {
					const partToAdd = res.data.part;
					const indexInParts = this.parts.findIndex(part => part.id === partToAdd.id);
					if (indexInParts > -1) {
						if (this.parts[indexInParts].amount > 1) {
							this.parts[indexInParts].amount -= 1;
						} else {
							this.parts.splice(indexInParts, 1);
						}
					}
					const indexInBilledParts = this.billedParts.findIndex(part => part.itemNumber === partToAdd.itemNumber);

					if (indexInBilledParts > -1) {
						this.billedParts[indexInBilledParts].amount += 1;
					} else {
						partToAdd.amount = 1;
						this.billedParts.push(partToAdd);
					}

					this.calculateSum();
				}).catch(error => {
					console.error(error);
				});
		},
		addWorkToBill() {
			const work = {
				'id': this.workIndex,
				'itemNumber': 'Munka',
				'name': this.addWork,
				'amount': this.amount,
				'price': this.workPrice
			}
			this.billedParts.push(work);
			this.workIndex++;
			this.addWork = '';
			this.amount = '';
			this.workPrice = '';
			this.calculateSum();
		},
		deleteRow(id) {
			const indexInBilledParts = this.billedParts.findIndex(part => part.id === id);

			if (indexInBilledParts !== -1) {
				const deletedPart = this.billedParts[indexInBilledParts];

				if (deletedPart.amount > 1) {
					this.billedParts[indexInBilledParts].amount -= 1;
				} else {
					this.billedParts.splice(indexInBilledParts, 1);
				}

				const indexInParts = this.parts.findIndex(part => part.id === deletedPart.id);

				if (indexInParts !== -1 && deletedPart.id < Number.MAX_SAFE_INTEGER) {
					this.parts[indexInParts].amount += 1;
				} else if (deletedPart.id < 1000) {
					this.parts.push({ ...deletedPart, amount: 1 });
				}

				this.calculateSum();
			}
		},
		calculateSum() {
			let sum = 0;
			if (this.billedParts.length > 0) {
				sum = this.billedParts.reduce((acc, part) => acc + (part.price * part.amount), 0);
			}
			let sumWithTax = Math.ceil(sum * 1.27).toLocaleString();
			this.sum = sum.toLocaleString();
			this.sumWithTax = sumWithTax;
		},
		createBill() {
			let bill = {
				paramId: this.paramId,
				paramName: this.paramName,
				paramAddress: this.paramAddress,
				paramPostalCode: this.paramPostalCode,
				paramSettlement: this.paramSettlement,
				paramTaxNumber: this.paramTaxNumber,
				billedParts: this.billedParts.map(part => ({
					id: part.id,
					itemNumber: part.itemNumber,
					name: part.name,
					amount: part.amount,
					price: part.price
				})),
				sum: this.sum,
				sumWithTax: this.sumWithTax
			};
			console.log(bill);
			const path = 'http://localhost:5000/createBill';
			axios
				.post(path, bill, {
					headers: {
						'Content-Type': 'application/json',
					},
					responseType: 'blob',
				})
				.then((response) => {
					const blob = new Blob([response.data], { type: 'application/pdf' });
					const url = URL.createObjectURL(blob);
					window.open(url, '_blank');

					router.push({
						name: 'Customers',
						query: {
							successful: true
						}
					});
				})
				.catch((error) => {
					console.error('Error generating bill:', error);
					notify('error', 'Sikertelen számla elkészítés!');
				});
		}
	},
	computed: {
		displayedParts() {
			const filteredParts = this.parts.filter(part => {
				return Object.values(part).some(value => {
					if (typeof value === 'string') {
						return value.toLowerCase().includes(this.searchQuery.toLowerCase());
					}
					return false;
				})
			});
			return filteredParts.sort((a, b) => {
				if (a.name < b.name) return -1;
				if (a.name > b.name) return 1;
				return 0;
			});
		},
	},
	created() {
		this.getParts()
	}
};
</script>