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
			<table className={`table-auto`}>
					<thead className="text-gray-400 text-left">
						<th style={{'font-weight': 'normal', 'width': `${sdata.col_1}px`}} className="py-1"></th>
						<th></th>
						<th style={{'font-weight': 'normal'}} className="py-1"></th>
						<th style={{'font-weight': 'normal'}} className="py-1"></th>
						<th style={{'font-weight': 'normal'}} className="py-1"></th>
						<th style={{'font-weight': 'normal'}} className="py-1"></th>
					</thead>
					<tbody>
							<tr>
								<td className="text-gray-400 text-left">{rule_type}</td>
								<td></td>
								<td className="text-gray-400 text-left">(INC VAT)</td>
								<td className="text-gray-400 text-left">(EXC VAT)</td>
								<td className="text-gray-400 text-left"></td>
								<td className="text-gray-400 text-left"></td>
						</tr>
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
  const [edit_trade, setEditTrade] = useState(false)
  const [edit_tradeNoVat, setEditTradeNoVat] = useState(false)
  const [edit_list, setEditList] = useState(false)
  const [edit_listNoVat, setEditListNoVat] = useState(false)

	const [rule_type, setRecord] = useState(price_record.rule_type)
	const [display_one, setOne] = useState(price_record.rule_display_1)
	const [display_two, setTwo] = useState(price_record.rule_display_2)
	const [list, setList] = useState(price_record.gbp_price)
	const [listNoVat, setListNoVat] = useState(price_record.gbp_price_no_vat)
	const [trade, setTrade] = useState(price_record.gbp_trade)
	const [tradeNoVat, setTradeNoVat] = useState(price_record.gbp_trade_no_vat)

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
  }, [rule_type, display_one, display_two, listNoVat, trade, tradeNoVat])


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
					<td style={{'width':`${sdata.col_1}px`}} onClick={ () => onClickHandler(setEditOne) } >{display_one}</td>
					<td style={{'width':`${sdata.col_2}px`}} onClick={ () => onClickHandler(setEditTwo) } >{display_two}</td>
					<td style={{'font-weight': 'bold', 'width':`${sdata.col_3}px`}}  onClick={() => { onClickHandler(setEditList) }} >£{list}</td>
					<td style={{'width':`${sdata.col_4}px`}} onClick={ () => { onClickHandler(setEditListNoVat)} } >£{listNoVat}</td>
					<td style={{'width':`${sdata.col_5}px`}} onClick={ () => { onClickHandler(setEditTrade)} } ></td>
					<td style={{'width':`${sdata.col_6}px`}} onClick={ () => { onClickHandler(setEditTradeNoVat)} } ></td>
			</tr>
		</>
	)
}
