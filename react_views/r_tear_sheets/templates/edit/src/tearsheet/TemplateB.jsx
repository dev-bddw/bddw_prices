import {useEffect, useRef, useState} from 'react'
import {
	DndContext,
	closestCenter,
	KeyboardSensor,
	PointerSensor,
	useSensor,
	useSensors,
} from '@dnd-kit/core'
import {
	arrayMove,
	SortableContext,
	sortableKeyboardCoordinates,
	useSortable,
	verticalListSortingStrategy,
} from '@dnd-kit/sortable'
import {CSS} from '@dnd-kit/utilities'

//TWO COLUMN
export default function TemplateB({price_records, sdata, setPriceRecords, tearsheet_id}) {
	return(
		<>
			{/*iterate over the price records objects, each object key == rule type, value = the list of price record objects*/}
			{  price_records.map(  ( obj )  => { return( Object.entries(obj).map( ([key, value]) => { return( <RuleTypeGroup key={key} sdata={sdata} price_records={value} rule_type={key} setPriceRecords={setPriceRecords} price_records_all={price_records} tearsheet_id={tearsheet_id} />)})) })}
		</>
	)
}

function RuleTypeGroup({sdata, price_records, rule_type, setPriceRecords, price_records_all, tearsheet_id}) {
	const [items, setItems] = useState(price_records)
	
	const sensors = useSensors(
		useSensor(PointerSensor),
		useSensor(KeyboardSensor, {
			coordinateGetter: sortableKeyboardCoordinates,
		})
	)

	useEffect(() => {
		setItems(price_records)
	}, [price_records])

	const handleVisibilityToggle = (recordId, isActive) => {
		if (!isActive) {
			// Remove from local items
			setItems(items.filter(item => 
				(item.selection_id || item.id) !== recordId
			))
			
			// Update parent state
			const updatedPriceRecords = price_records_all.map(obj => {
				const entries = Object.entries(obj)
				const [key, value] = entries[0]
				if (key === rule_type) {
					return {[key]: value.filter(item => 
						(item.selection_id || item.id) !== recordId
					)}
				}
				return obj
			})
			setPriceRecords(updatedPriceRecords)
		}
	}

	function handleDragEnd(event) {
		const {active, over} = event

		if (over && active.id !== over.id) {
			setItems((items) => {
				const oldIndex = items.findIndex(item => (item.selection_id || item.id) === active.id)
				const newIndex = items.findIndex(item => (item.selection_id || item.id) === over.id)
				const newItems = arrayMove(items, oldIndex, newIndex)
				
				// Update the parent price_records state
				const updatedPriceRecords = price_records_all.map(obj => {
					const entries = Object.entries(obj)
					const [key, value] = entries[0]
					if (key === rule_type) {
						return {[key]: newItems}
					}
					return obj
				})
				setPriceRecords(updatedPriceRecords)
				
				// Collect all selection IDs across all rule types in order
				const allSelectionIds = []
				updatedPriceRecords.forEach(obj => {
					const entries = Object.entries(obj)
					const [key, value] = entries[0]
					value.forEach(item => {
						if (item.selection_id) {
							allSelectionIds.push(item.selection_id)
						} else if (item.id) {
							// Fallback: if no selection_id, we can't reorder via API
							// This shouldn't happen with the updated helper, but handle gracefully
							console.warn('Price record missing selection_id:', item)
						}
					})
				})
				
				// Call API to update order for all records
				reorderPriceRecords(allSelectionIds)
				
				return newItems
			})
		}
	}

	function reorderPriceRecords(selectionIds) {
		fetch(`/api/tearsheets/${tearsheet_id}/reorder_records/`, {
			credentials: 'include',
			mode: 'same-origin',
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				"Accept": 'application/json',
				'Authorization': `Token ${CONTEXT.auth_token}`,
				'X-CSRFToken': CONTEXT.csrf_token
			},
			body: JSON.stringify({
				'record_ids': selectionIds
			}),
		})
		.then(response => response.json())
		.then(data => {
			console.log('Reorder success:', data);
		})
		.catch(error => {
			console.error('Reorder error:', error);
		})
	}

	return(
		<>
			<div style={{'height': sdata.pt_pr}}></div>
			<DndContext
				sensors={sensors}
				collisionDetection={closestCenter}
				onDragEnd={handleDragEnd}
			>
				<table className={`table-auto`}>
					<thead className="text-gray-400 text-left">
						<th style={{'width': '20px'}}></th>
						<th style={{'width': '30px'}}></th>
						<th></th>
						<th></th>
						<th></th>
						<th style={{'font-weight': 'normal'}} className="py-1">LIST</th>
						<th style={{'font-weight': 'normal'}} className="py-1">NET</th>
					</thead>
					<tbody>
						<SortableContext items={items.map(item => item.selection_id || item.id)} strategy={verticalListSortingStrategy}>
							{items.map( (price_record, index) =>  
								<TableRow 
									key={price_record.selection_id || price_record.id} 
									sdata={sdata} 
									index={index} 
									price_record={price_record}
									tearsheet_id={tearsheet_id}
									onToggleVisibility={handleVisibilityToggle}
								/>
							)}
						</SortableContext>
					</tbody>
				</table>
			</DndContext>
		</>
	)
}

function TableRow({sdata, price_record, index, tearsheet_id, onToggleVisibility}) {
	const {
		attributes,
		listeners,
		setNodeRef,
		transform,
		transition,
		isDragging,
	} = useSortable({id: price_record.selection_id || price_record.id})

	const style = {
		transform: CSS.Transform.toString(transform),
		transition,
		opacity: isDragging ? 0.5 : 1,
	}

	const [edit_type, setEditType] = useState(false)
	const [edit_one, setEditOne] = useState(false)
	const [edit_two, setEditTwo] = useState(false)
	const [edit_list, setEditList] = useState(false)
	const [edit_net, setEditNet] = useState(false)

	const [rule_type, setRecord] = useState(price_record.rule_type)
	const [display_one, setOne] = useState(price_record.rule_display_1)
	const [display_two, setTwo] = useState(price_record.rule_display_2)
	const [list, setList] = useState(price_record.list_price)
	const [net, setNet] = useState(price_record.net_price)
	const [isVisible, setIsVisible] = useState(true) // All shown records are active by default

	const isMounted = useRef(false)
	const onClickHandler = (setter) => {
		setter(true)
	}

	const onChangeHandler = (event, setter) => {
		setter(event.target.value)
	}

	const handleVisibilityToggle = async (e) => {
		e.stopPropagation() // Prevent row click events
		const recordId = price_record.id
		const recordType = 'price_record' // Default to price_record, could be enhanced to detect formula_price_record
		
		try {
			const response = await fetch(
				`/api/tearsheets/${tearsheet_id}/toggle-record/${recordId}/`,
				{
					credentials: 'include',
					mode: 'same-origin',
					method: "POST",
					headers: {
						"Content-Type": "application/json",
						"Accept": 'application/json',
						'Authorization': `Token ${CONTEXT.auth_token}`,
						'X-CSRFToken': CONTEXT.csrf_token
					},
					body: JSON.stringify({
						'type': recordType
					}),
				}
			)
			
			const data = await response.json()
			
			if (response.ok) {
				setIsVisible(data.is_active)
				// If hidden, remove from view
				if (!data.is_active && onToggleVisibility) {
					onToggleVisibility(recordId, data.is_active)
				}
			} else {
				console.error('Toggle visibility error:', data)
			}
		} catch (error) {
			console.error('Toggle visibility error:', error)
		}
	}

	// add a delay, then execute the api call on cleanup
	useEffect(() => {
		const delayDebounceFn = setTimeout(() => {
			if (isMounted.current) {
				UPDATE()
			} else {
				isMounted.current = true
			}
		}, 1500)
		return( () => clearTimeout(delayDebounceFn) )
	}, [rule_type, display_one, display_two, list, net])


	const UPDATE = () => {
		fetch(CONTEXT.edit_pricerecord_api, {
			credentials: 'include',
			mode: 'same-origin',
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				"Accept": 'application/json',
				'Authorization': `Token ${CONTEXT.auth_token}`,
				'X-CSRFToken': CONTEXT.csrf_token
			},
			body: JSON.stringify({'data':[{
				'id': price_record.id,
				'rule_type': rule_type,
				'rule_display_1': display_one,
				'rule_display_2': display_two,
				'list_price': list,
				'net_price': net
			}] }),
		})
		.then(response => response.json())
		.then(data => {
			console.log(data);
		})
	}

	const classes="shadow appearance-none border rounded w-full py-1 text-gray-700 leading-tight focus:outline-none focus:shadow-outliney-1"

	return(
		<>
			<tr ref={setNodeRef} style={style} className="hover:bg-gray-50 text-gray-400 text-left">
				<td {...attributes} {...listeners} style={{'width': '20px', 'cursor': 'grab'}} className="text-gray-300 hover:text-gray-500">
					<svg width="12" height="12" viewBox="0 0 12 12" fill="currentColor">
						<circle cx="2" cy="2" r="1"/>
						<circle cx="6" cy="2" r="1"/>
						<circle cx="10" cy="2" r="1"/>
						<circle cx="2" cy="6" r="1"/>
						<circle cx="6" cy="6" r="1"/>
						<circle cx="10" cy="6" r="1"/>
						<circle cx="2" cy="10" r="1"/>
						<circle cx="6" cy="10" r="1"/>
						<circle cx="10" cy="10" r="1"/>
					</svg>
				</td>
				<td style={{'width': '30px', 'text-align': 'center'}} onClick={(e) => e.stopPropagation()}>
					<input
						type="checkbox"
						checked={isVisible}
						onChange={handleVisibilityToggle}
						title={isVisible ? "Hide this record" : "Show this record"}
						style={{'cursor': 'pointer'}}
					/>
				</td>
				{
				edit_type ?
					<td style={{'width': `${sdata.col_1}px`}}><input onChange={ (event) => onChangeHandler(event,setRecord)} className={classes} value={rule_type}></input></td>
					:<td style={{'width': `${sdata.col_1}px`}} onClick={ () => onClickHandler(setEditType) } >{ index == 0 ? rule_type : null}</td>
				}{
				edit_one ?
					<td style={{'width': `${sdata.col_2}px`}}><input onChange={ (event) => onChangeHandler(event,setOne)} className={classes} value={display_one}></input></td>
					:<td style={{'width':`${sdata.col_2}px`}} onClick={ () => onClickHandler(setEditOne) } >{display_one}</td>
				}{
				edit_two ?
					<td style={{'width':`${sdata.col_3}px`}}><input onChange={ (event) => onChangeHandler(event,setTwo)} className={classes} value={display_two}></input></td>
					:<td style={{'width':`${sdata.col_3}px`}} onClick={ () => onClickHandler(setEditTwo) } >{display_two}</td>
				}{
				edit_list ?
					<td style={{'width':`${sdata.col_4}px`}}><input onChange={ (event) => onChangeHandler(event,setList)} className={classes} value={list}></input></td>
					:<td style={{'width':`${sdata.col_4}px`}}  onClick={() => { onClickHandler(setEditList) }}>${list}</td>
				}
				{
				edit_net ?
					<td style={{'width':`${sdata.col_5}px`}}><input onChange={ (event) => onChangeHandler(event,setNet)} className={classes} value={net}></input></td>
					:<td style={{'width':`${sdata.col_5}px`}} onClick={ () => { onClickHandler(setEditNet)} } >${net}</td>
				}
			</tr>
		</>
	)
}
