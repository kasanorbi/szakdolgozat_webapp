<template>
	<div class="flex flex-col w-max-screen-lg mx-[15vw]">
		<div class="">
			<h1 class="w-full text-center text-7xl mt-[3vh] font-extrabold">Partnerek</h1>
			<div class="divider" />
			<div class="flex justify-between w-full">
				<div class="flex gap-6">
					<button type="button" class="btn btn-primary" @click="toggleAddCustomerModal">
						<span class="material-symbols-outlined"> person_add </span>
						<span>Új partner felvétele</span>
					</button>
				</div>
				<div class="flex gap-6">
					<label class="input input-bordered flex items-center gap-2">
						<input type="text" class="grow" placeholder="Keresés" v-model="searchQuery" />
					</label>
					<label class="label cursor-pointer flex gap-2">
						<span class="label-text text-lg">Csak cégek megjelenítése</span>
						<input type="checkbox" id="cbx-3" v-model="justCompanies" class="toggle" />
					</label>
				</div>
			</div>
		</div>
		<div class="overflow-x-auto mt-[3vh]">
			<table class="table">
				<thead class="text-2xl text-center">
					<tr>
						<th @click="sortByColumn('name')" class="hover:cursor-pointer">Név</th>
						<th>Adószám</th>
						<th @click="sortByColumn('settlement')" class="hover:cursor-pointer">
							<span class="scale-150 material-symbols-outlined">
								home
							</span>
						</th>
						<th @click="sortByColumn('email')" class="hover:cursor-pointer">
							<span class="scale-150 material-symbols-outlined">
								mail
							</span>
						</th>
					</tr>
				</thead>
				<tbody>
					<template v-if="displayedCustomers.length > 0">
						<tr v-for="(customer, index) in displayedCustomers" :key="index">
							<td class="text-left text-lg">{{ customer.name }}</td>
							<td class="text-left text-lg">{{ customer.taxNumber }}</td>
							<td class="text-left text-lg">{{ customer.postalCode }}, {{ customer.settlement }} {{
								customer.address }}</td>
							<td class="text-left text-lg">{{ customer.email }}</td>
							<td>
								<div class="flex gap-2">
									<button type="button" class="btn btn-success hover:scale-110"
										title="Számla kiállítása"
										@click="createBill(customer.id, customer.name, customer.taxNumber, customer.postalCode, customer.settlement, customer.address)">
										<span class="material-symbols-outlined"> receipt_long </span>
									</button>
									<button type="button" class="btn btn-warning hover:scale-110"
										@click="toggleUpdateCustomerModal(customer.id)" title="Adatok módosítása">
										<span class="material-symbols-outlined"> person_edit </span>
									</button>
									<button type="button" class="btn btn-error hover:scale-110"
										@click="deleteCustomer(customer.id)" title="Törlés">
										<span class="material-symbols-outlined"> delete </span>
									</button>
								</div>
							</td>
						</tr>
					</template>
					<template v-else>
						<tr>
							<td colspan="9" class="text-center mt-4 text-3xl">
								Nem található ilyen partner.
							</td>
						</tr>
					</template>
				</tbody>
			</table>
		</div>
	</div>
	<div v-if="activeAddCustomerModal"
		class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
		<div class="modal modal-open">
			<div class="modal-box">
				<div class="modal-header">
					<h1 class="text-2xl text-center w-full">Új partner felvétele</h1>
				</div>
				<div class="modal-body">
					<form>
						<div class="mb-3">
							<label for="addCustomerName" class="label">Név:</label>
							<input type="text" class="input input-bordered w-full" id="addCustomerName"
								v-model="addCustomerForm.name" placeholder="Név megadása" />
						</div>
						<div class="mb-3">
							<label for="addCustomerPostalCode" class="label">Irányítószám</label>
							<input type="text" class="input input-bordered w-full" id="addCustomerPostalCode"
								v-model="addCustomerForm.postalCode" placeholder="Irányítószám megadása" />
						</div>
						<div class="mb-3">
							<label for="addCustomerSettlement" class="label">Település:</label>
							<input type="text" class="input input-bordered w-full" id="addCustomerSettlement"
								v-model="addCustomerForm.settlement" placeholder="Település megadása" />
						</div>
						<div class="mb-3">
							<label for="addCustomerAddress" class="label">Lakcím:</label>
							<input type="text" class="input input-bordered w-full" id="addCustomerAddress"
								v-model="addCustomerForm.address" placeholder="Lakcím megadása" />
						</div>
						<div class="mb-3">
							<label for="addCustomerTaxNumber" class="label">Adószám:</label>
							<input type="text" class="input input-bordered w-full" id="addCustomerTaxNumber"
								v-model="addCustomerForm.taxNumber" placeholder="Adószám megadása" />
						</div>
						<div class="mb-3">
							<label for="addCustomerEmail" class="label">Email:</label>
							<input type="email" class="input input-bordered w-full" id="addCustomerEmail"
								v-model="addCustomerForm.email" placeholder="Email cím megadása" />
						</div>
						<div class="flex justify-between">
							<div>
								<button type="button" class="btn btn-primary" @click="handleAddSubmit">
									Hozzáadás
								</button>
								<button type="button" class="btn btn-primary ml-2" @click="initForm">
									Alaphelyzetbe állítás
								</button>
							</div>
							<div>
								<button type="button" class="btn btn-secondary" @click="toggleAddCustomerModal">
									Mégse
								</button>
							</div>
						</div>
					</form>
				</div>
			</div>
		</div>
	</div>
	<!-- Update Customer Modal -->
	<div v-if="activeUpdateCustomerModal"
		class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
		<div class="modal modal-open">
			<div class="modal-box">
				<div class="modal-header">
					<h1 class="text-2xl text-center w-full">Partner módosítása</h1>
				</div>
				<form class="flex flex-col gap-4">
					<div class="">
						<input type="text" class="input input-bordered w-full hidden" id="updateCustomerId"
							v-model="updateCustomerForm.id" readonly="readonly" />
						<label for="updateCustomerName" class="label">Név:</label>
						<input type="text" class="input input-disabled w-full" id="updateCustomerName"
							v-model="updateCustomerForm.name" readonly="readonly" />
					</div>
					<div class="">
						<label for="updateCustomerPostalCode" class="label">Irányítószám</label>
						<input type="text" class="input input-bordered w-full" id="updateCustomerPostalCode"
							v-model="updateCustomerForm.postalCode" placeholder="Irányítószám megadása" />
					</div>
					<div class="">
						<label for="updateCustomerSettlement" class="label">Település:</label>
						<input type="text" class="input input-bordered w-full" id="updateCustomerSettlement"
							v-model="updateCustomerForm.settlement" placeholder="Település megadása" />
					</div>
					<div class="">
						<label for="updateCustomerAddress" class="label">Lakcím:</label>
						<input type="text" class="input input-bordered w-full" id="updateCustomerAddress"
							v-model="updateCustomerForm.address" placeholder="Lakcím megadása" />
					</div>
					<div class="">
						<label for="updateCustomerTaxNumber" class="label">Adószám:</label>
						<input type="text" class="input input-bordered w-full" id="updateCustomerTaxNumber"
							v-model="updateCustomerForm.taxNumber" placeholder="Adószám megadása" />
					</div>
					<div class="">
						<label for="updateCustomerEmail" class="label">Email:</label>
						<input type="email" class="input input-bordered w-full" id="updateCustomerEmail"
							v-model="updateCustomerForm.email" placeholder="Email cím megadása" />
					</div>
					<div class="flex justify-between">
						<button type="button" class="btn btn-primary" @click="handleUpdateSubmit">
							Módosítás
						</button>
						<button type="button" class="btn btn-secondary" @click="toggleUpdateCustomerModal">
							Mégse
						</button>
					</div>
				</form>
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
	if (type == 'success') {
		toast.success(message, {
			theme: 'dark',
			position: toast.POSITION.TOP_RIGHT,
		});
	} else if (type == 'error') {
		toast.error(message, {
			theme: 'dark',
			position: toast.POSITION.TOP_RIGHT,
		});
	} else if (type == 'info') {
		toast.info(message, {
			theme: 'dark',
			position: toast.POSITION.TOP_RIGHT,
		})
	}
}
export default {
	props: ['successful'],
	data() {
		return {
			activeAddCustomerModal: false,
			activeUpdateCustomerModal: false,
			customers: [],
			nextCustomerIndex: 0,
			sortBy: 'name',
			sortDirection: 'asc',
			searchQuery: '',
			justCompanies: false,
			addCustomerForm: {
				name: '',
				postalCode: '',
				settlement: '',
				address: '',
				taxNumber: '',
				email: '',
			},
			updateCustomerForm: {
				id: '',
				...this.addCustomerForm
			}
		};
	},
	methods: {
		getCustomers() {
			const path = 'http://localhost:5000/getCustomers';
			axios.get(path).then((res) => {
				this.customers = Object.values(res.data.customers);
				this.nextCustomerIndex = res.data.nextCustomerIndex;
				console.log(activeAddCustomerModal)
				if (successful) {
					notify('success', 'Sikeres számla kiállítás!');
					successful = false;
				}
			}).catch((error) => {
				console.error(error);
			});
		},
		addCustomer(payload) {
			const path = 'http://localhost:5000/addCustomer';
			axios.post(path, payload, {
				headers: {
					'Content-Type': 'application/json',
				},
			}).then(() => {
				notify('success', 'Partner sikeresen hozzáadva!')
				this.getCustomers();
			}).catch((error) => {
				console.log(error);
				this.getCustomers();
			})
		},
		updateCustomer(payload) {
			const path = 'http://localhost:5000/updateCustomer';
			axios.post(path, payload, {
				headers: {
					'Content-Type': 'application/json',
				},
			}).then(() => {
				this.getCustomers();
			}).catch((error) => {
				console.log(error);
				this.getCustomers();
			})
		},
		deleteCustomer(payload) {
			const path = 'http://localhost:5000/deleteCustomer';
			axios.post(path, payload, {
				headers: {
					'Content-Type': 'application/json',
				},
			}).then(() => {
				notify('info', 'Partner eltávolítva a listából!')
				this.getCustomers();
			}).catch((error) => {
				notify('error', 'Nem sikerült művelet!')
				this.getCustomers();
			})
		},
		handleAddSubmit() {
			this.toggleAddCustomerModal();
			const { name, postalCode, settlement, address, taxNumber, email } = this.addCustomerForm;
			const payload = { id: this.nextCustomerIndex, name, postalCode, settlement, address, taxNumber, email };
			this.addCustomer(payload);
			this.initForm();
		},
		handleUpdateSubmit() {
			this.toggleUpdateCustomerModal(-1);
			const { id, name, postalCode, settlement, address, taxNumber, email } = this.updateCustomerForm;
			const payload = { id, name, postalCode, settlement, address, taxNumber, email };
			this.updateCustomer(payload);
		},
		initForm() {
			this.addCustomerForm = {};
		},
		initUpdateForm(customerId) {
			const customerToUpdate = this.customers.find(customer => customer.id === customerId);
			if (customerToUpdate) {
				this.updateCustomerForm = { ...customerToUpdate };
			}
		},
		toggleAddCustomerModal() {
			const body = document.querySelector('body');
			this.activeAddCustomerModal = !this.activeAddCustomerModal;
			body.classList.toggle('modal-open', this.activeAddCustomerModal);
		},
		toggleUpdateCustomerModal(customerId) {
			const body = document.querySelector('body');
			this.activeUpdateCustomerModal = !this.activeUpdateCustomerModal;
			customerId !== -1 && this.initUpdateForm(customerId);
		},
		sortByColumn(column) {
			if (column === this.sortBy) {
				this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
			} else {
				this.sortBy = column;
				this.sortDirection = 'asc';
			}
		},
		justCompaniesToggler() {
			this.justCompanies = !this.justCompanies;
		},
		createBill(id, name, taxNumber, postalCode, settlement, address) {
			router.push({
				name: 'Billing',
				query: {
					paramId: id,
					paramName: name,
					paramTaxNumber: taxNumber,
					paramPostalCode: postalCode,
					paramSettlement: settlement,
					paramAddress: address
				}
			});
		}
	},
	computed: {
		displayedCustomers() {
			const filteredCustomers = this.customers.filter(person => {
				return Object.values(person).some(value => {
					if (typeof value === 'string') {
						return value.toLowerCase().includes(this.searchQuery.toLowerCase());
					}
					return false;
				})
			});
			const filteredCustomersJustCompanies = this.customers.filter(company => {
				return Object.values(company).some(value => {
					if (typeof value === 'string') {
						const lowerCaseValue = value.toLowerCase();
						const lowerCaseQuery = this.searchQuery.toLowerCase();
						const includesSearchQuery = lowerCaseValue.includes(lowerCaseQuery);
						const includesAdditionalKeywords = ["kft", "zrt", "bt", "ltd"].some(keyword => lowerCaseValue.includes(keyword));
						return includesSearchQuery && includesAdditionalKeywords;
					}
				})
			});
			if (this.justCompanies) {
				return filteredCustomersJustCompanies.sort((a, b) => {
					let modifier = 1;
					if (this.sortDirection === 'desc') modifier = -1;
					if (a[this.sortBy] < b[this.sortBy]) return -1 * modifier;
					if (a[this.sortBy] > b[this.sortBy]) return 1 * modifier;
					return 0;
				});
			} else {
				return filteredCustomers.sort((a, b) => {
					let modifier = 1;
					if (this.sortDirection === 'desc') modifier = -1;
					if (a[this.sortBy] < b[this.sortBy]) return -1 * modifier;
					if (a[this.sortBy] > b[this.sortBy]) return 1 * modifier;
					return 0;
				});
			}
		},
	},
	mounted() {
		this.getCustomers();
	},
	created() {
		this.getCustomers();
	},
};
</script>