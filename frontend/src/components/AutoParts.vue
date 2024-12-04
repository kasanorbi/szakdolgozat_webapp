<template>
	<div class="flex flex-col w-max-screen-lg mx-[15vw]">
		<div class="">
			<h1 class="w-full text-center text-7xl mt-[3vh] font-extrabold">Készlet</h1>
			<div class="divider" />
				<div class="flex justify-between mb-[3vh]">
					<div class="flex gap-6">
						<button type="button" class="btn btn-primary" @click="toggleAddPartModal">
							<span class="material-symbols-outlined">add</span>
							<span> Alkatrész hozzáadása</span>
						</button>
						<button type="button" class="btn btn-primary" @click="scanPart">
							<span class="material-symbols-outlined">document_scanner</span>
							<span> Számla beolvasása</span>
						</button>
					</div>
					<div>
						<label class="input input-bordered flex items-center gap-2">
							<input type="text" id="search" class="grow" v-model="searchQuery" placeholder="Keresés">
						</label>
					</div>
				</div>
			<div class="overflow-x-auto flex justify-center">
				<table class="table w-[80vw]">
					<thead class="text-2xl text-center">
						<tr>							
							<th @click="sortByColumn('name')" class="sortable">Megnevezés</th>
							<th @click="sortByColumn('amount')" class="sortable">Mennyiség</th>
							<th @click="sortByColumn('price')" class="sortable">Nettó</th>
							<th>Bruttó</th>
						</tr>
					</thead>
					<tbody>
						<template v-if="displayedParts.length > 0">
							<tr v-for="(part, index) in displayedParts" :key="index">
								<td class="text-left text-lg">{{ part.name }}</td>
								<td class="text-lg">{{ part.amount }} db</td>
								<td class="text-lg">{{ Math.ceil(part.price) }}Ft</td>
								<td class="text-lg">{{ Math.ceil((part.price) * 1.27) }}Ft</td>
								<td class="flex">
									<button type="button" class="btn btn-warning hover:scale-110" title="Módosítás"
										style="scale: 0.8;"
										@click="toggleUpdatePartModal(part.id, part.amount, part.itemNumber, part.name, part.price)">
										<span class="material-symbols-outlined"> edit </span>
									</button>
									<button type="button" class="btn btn-error hover:scale-110" title="Törlés"
										style="margin-left: 0.2rem; scale: 0.8;" @click="deletePart(part.id)">
										<span class="material-symbols-outlined"> delete </span>
									</button>
								</td>
							</tr>
						</template>
						<template v-else>
							<tr>
								<td colspan="9" class="text-center mt-4 text-3xl">
									Nem található ilyen alkatrész.
								</td>
							</tr>
						</template>
					</tbody>
				</table>
			</div>
		</div>
	</div>
	<div v-if="activateAddPartModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black-opacity-50">
		<div class="modal modal-open">
			<div class="modal-box">
				<div class="modal-header">
					<h1 class="text-2xl text-center w-full">Alkatrész felvétele</h1>
				</div>
				<form class="flex flex-col gap-4">
					<div>
						<label for="addPartItemNumber" class="label">Cikkszám:</label>
						<input type="text" class="input input-bordered w-full" id="addPartItemNumber"
							v-model="addPartForm.itemNumber" placeholder="Cikkszám">
					</div>
					<div>
						<label for="addPartName" class="label">Megnevezés:</label>
						<input type="text" class="input input-bordered w-full" id="addPartName"
							v-model="addPartForm.name" placeholder="Megnevezés">
					</div>
					<div>
						<label for="addPartAmount" class="label">Mennyiség:</label>
						<input type="number" class="input input-bordered w-full" id="addPartAmount"
							v-model="addPartForm.amount" placeholder="Mennyiség">
					</div>
					<div>
						<label for="addPartPrice" class="label">Ár:</label>
						<input class="input input-bordered w-full" id="addPartPrice" v-model="addPartForm.price"
							placeholder="5000 Ft">
					</div>
					<div class="flex justify-between">
						<div>
							<button type="button" class="btn btn-primary" @click="handleAddSubmit">
								<span>Hozzáadás</span>
							</button>
							<button style="margin-left: 10px;" type="button" class="btn btn-primary" @click="initForm">
								<span>Alaphelyzetbe állítás</span>
							</button>
						</div>
						<div>
							<button type="button" class="btn btn-secondary" @click="toggleAddPartModal">Mégse</button>
						</div>
					</div>
				</form>
			</div>
		</div>
	</div>

	<div ref="updatePartModal" class="modal fade"
		:class="{ show: activateUpdatePartModal, 'd-block': activateUpdatePartModal }" tabindex="-1" role="dialog">
		<div class="modal-dialog" role="document">
			<div class="modal-content">
				<div class="modal-header">
					<h5 class="modal-title">Alkatrész módosítása</h5>
					<button type="button" class="btn-close" data-dismiss="modal"
						@click="toggleUpdatePartModal"></button>
				</div>
				<div class="modal-body">
					<form>
						<div class="mb-3">
							<input type="text" id="updatePartId" v-model="updatePartForm.id" hidden>
							<label for="updatePartItemNumber" class="form-label">Cikkszám</label>
							<input type="text" class="form-control" id="updatePartItemNumber"
								v-model="updatePartForm.itemNumber" placeholder="Cikkszám">
						</div>
						<div class="mb-3">
							<label for="updatePartName" class="form-label">Megnevezés:</label>
							<input type="text" class="input_field" id="updatePartName" v-model="updatePartForm.name"
								placeholder="Megnevezés">
						</div>
						<div class="mb-3">
							<label for="updatePartAmount" class="form-label">Mennyiség:</label>
							<input type="number" class="input_field" id="updatePartAmount"
								v-model="updatePartForm.amount">
						</div>
						<div class="mb-3">
							<label for="updatePartPrice" class="form-label">Ár (Ft):</label>
							<input type="text" class="input_field" id="updatePartPrice" v-model="updatePartForm.price"
								placeholder="5000 Ft">
						</div>
						<button type="button" class="button-prim" @click="handleUpdateSubmit"> Módosítás </button>
					</form>
				</div>
			</div>
		</div>
	</div>
	<div v-if="activateUpdatePartModal" class="modal-backdrop fade show"></div>
</template>
<script>
import axios from 'axios';
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';
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
	}
}
export default {
	data() {
		return {
			activateAddPartModal: false,
			addPartForm: {
				itemNumber: '',
				name: '',
				amount: '',
				price: '',
			},
			activateUpdatePartModal: false,
			updatePartForm: {
				id: '',
				itemNumber: '',
				name: '',
				amount: '',
				price: '',
			},
			parts: [],
			nextPartIndex: 0,
			sortBy: 'itemNumber',
			sortDirection: 'asc',
			searchQuery: '',
		};
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
		addPart(payload) {
			const path = 'http://localhost:5000/addComponent';
			axios.post(path, payload, {
				headers: {
					'Content-Type': 'application/json',
				},
			}).then(() => {
				notify('success', 'Alkatrész sikeresen hozzáadva!');
				this.getParts();
			}).catch((error) => {
				console.log(error);
				this.getParts();
			})
		},
		scanPart() {
			const path = 'http://localhost:5000/scan';
			axios.get(path).then((res) => {
				this.parts = res.data.parts;
				this.nextPartIndex = res.data.nextPartIndex;
			}).catch((error) => {
				if (error.response.status === 501) {
					notify('error', 'Nincs szkenner csatlakoztatva!');
				} else {
					console.error(error);
				}
			})
		},
		updatePart(payload) {
			const path = 'http://localhost:5000/updateComponent';
			axios.post(path, payload, {
				headers: {
					'Content-Type': 'application/json',
				},
			}).then(() => {
				this.getParts();
			}).catch((error) => {
				console.log(error);
				this.getParts();
			})
		},
		deletePart(payload) {
			const path = 'http://localhost:5000/deleteComponent';
			axios.post(path, payload, {
				headers: {
					'Content-Type': 'application/json',
				},
			}).then(() => {
				notify('success', 'Alkatrész eltávolítva a listából!');
				this.getParts();
			}).catch((error) => {
				notify('error', 'Nem sikerült művelet!');
				this.getParts();
			})
		},
		handleAddSubmit() {
			this.toggleAddPartModal();
			const { itemNumber, name, amount, price } = this.addPartForm;
			const payload = { id: this.nextPartIndex, itemNumber, name, amount, price };
			this.addPart(payload);
			this.initForm();
		},
		handleUpdateSubmit() {
			this.toggleUpdatePartModal(-1);
			const { id, itemNumber, amount, name, price } = this.updatePartForm;
			const payload = { id, itemNumber, amount, name, price };
			this.updatePart(payload);
		},
		initForm() {
			this.addPartForm = {};
		},
		initUpdateForm(partId) {
			const partToUpdate = this.parts.find(part => part.id === partId);
			if (partToUpdate) {
				this.updatePartForm = { ...partToUpdate };
			}
		},
		toggleAddPartModal() {
			const body = document.querySelector('body');
			this.activateAddPartModal = !this.activateAddPartModal;
			body.classList.toggle('modal-open', this.activateAddPartModal);
		},
		toggleUpdatePartModal(partId, partAmount, partItemNumber, partName, partPrice) {
			const body = document.querySelector('body');
			this.activateUpdatePartModal = !this.activateUpdatePartModal;
			body.classList.toggle('modal-open', this.activateUpdatePartModal);
			partId !== -1 && this.initUpdateForm(partId, partAmount, partItemNumber, partName, partPrice);
		},
		sortByColumn(column) {
			if (column === this.sortBy) {
				this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
			} else {
				this.sortBy = column;
				this.sortDirection = 'asc';
			}
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
				let modifier = 1;
				if (this.sortDirection === 'desc') modifier = -1;
				if (a[this.sortBy] < b[this.sortBy]) return -1 * modifier;
				if (a[this.sortBy] > b[this.sortBy]) return 1 * modifier;
				return 0;
			});
		},
	},
	mounted() {
		this.getParts();
	},
	created() {
		this.getParts();
	},
};
</script>