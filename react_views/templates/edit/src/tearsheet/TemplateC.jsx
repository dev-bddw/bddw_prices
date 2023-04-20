import {useEffect, useRef, useState} from 'react'

import SETTINGS from './Settings'


//RULE DISPLAY ABOVE
export default function TemplateA({price_records, sdata}) {
	return(
		<>
							{/*iterate over the price records objects, each objectL key == rule type, value = the list of price record objects*/}
								{  price_records.map(  ( obj )  => { return( Object.entries(obj).map( ([key, value]) => { return( <RuleTypeGroup sdata={sdata} price_records={value} rule_type={key} />)})) })}
								{/*<AddRow price_records={price_records} setPriceRecords={setPriceRecords} tearsheet_id={tearsheet_id}/>*/}
	</>
	)
}

function RuleTypeGroup({sdata, price_records, rule_type}) {
  //TODO rewrite so variables stay the same from model to user
  return(
		<>
			<div style={{'height': sdata.pt_pr}}></div>
			<table style={{'width': '850px'}} className={`mx-auto table-auto`}>
					<thead className="text-gray-400 text-left">
						<th style={{'font-weight': 'normal', 'width': `${sdata.col_1}%`}} className="py-1">{rule_type}</th>
						<th></th>
						<th style={{'font-weight': 'normal'}} className="py-1">LIST</th>
						<th style={{'font-weight': 'normal'}} className="py-1">NET</th>
					</thead>
					<tbody>
						{ price_records.map( (price_record, index) =>  <TableRow sdata={sdata} index={index} price_record={price_record} />)}
					</tbody>
			</table>
							</>
	)
}

function TableRow({sdata, price_record, index}) {
  //TODO rewrite so variables stay the same from model to user

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

	const isMounted = useRef(false)
	const onClickHandler = (setter) => {
	  setter(true)
	}

	const onChangeHandler = (event, setter) => {
	  setter(event.target.value)
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

  return(
		<>
		<tr key={index} className="hover:bg-gray-50 text-gray-400 text-left">
{
				edit_one ?
					<td style={{'width': `${sdata.col_2}%`}}><input onChange={ (event) => onChangeHandler(event,setOne)} className={SETTINGS.input_classes} value={display_one}></input></td>
					:<td style={{'width':`${sdata.col_2}%`}} onClick={ () => onClickHandler(setEditOne) } >{display_one}</td>
				}{
				edit_two ?
					<td style={{'width':`${sdata.col_3}%`}}><input onChange={ (event) => onChangeHandler(event,setTwo)} className={SETTINGS.input_classes} value={display_two}></input></td>
					:<td style={{'width':`${sdata.col_3}%`}} onClick={ () => onClickHandler(setEditTwo) } >{display_two}</td>
				}{
				edit_list ?
					<td style={{'width':`${sdata.col_4}%`}}><input onChange={ (event) => onChangeHandler(event,setList)} className={SETTINGS.input_classes} value={list}></input></td>
					:<td style={{'width':`${sdata.col_4}%`}}  onClick={() => { onClickHandler(setEditList) }} >${list}</td>
				}
				{
				edit_net ?
					<td style={{'width':`${sdata.col_5}%`}}><input onChange={ (event) => onChangeHandler(event,setNet)} className={SETTINGS.input_classes} value={net}></input></td>
					:<td style={{'width':`${sdata.col_5}%`}} onClick={ () => { onClickHandler(setEditNet)} } >${net}</td>
				}
			</tr>
		</>
	)
}
