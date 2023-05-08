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
						<th style={{'font-weight': 'normal'}} className="py-1">LIST</th>
						<th style={{'font-weight': 'normal'}} className="py-1"></th>
						<th style={{'font-weight': 'normal'}} className="py-1">TRADE</th>
						<th style={{'font-weight': 'normal'}} className="py-1"></th>
					</thead>
					<tbody>
							<tr>
								<td className="text-gray-400 text-left">{rule_type}</td>
								<td></td>
								<td className="text-gray-400 text-left">(INC VAT)</td>
								<td className="text-gray-400 text-left">(EXC VAT)</td>
								<td className="text-gray-400 text-left">(INC VAT)</td>
								<td className="text-gray-400 text-left">(EXC VAT)</td>
						</tr>
						{ price_records.map( (price_record, index) =>  <TableRow sdata={sdata} index={index} price_record={price_record} />)}
					</tbody>
			</table>
							</>
	)
}

function TableRow({sdata, price_record, index}) {
  //TODO rewrite so variables stay the same from model to user

	const [rule_type, setRecord] = useState(price_record.rule_type)
	const [display_one, setOne] = useState(price_record.rule_display_1)
	const [display_two, setTwo] = useState(price_record.rule_display_2)
	const [list, setList] = useState(price_record.gbp_price)
	const [listNoVat, setListNoVat] = useState(price_record.gbp_price_no_vat)
	const [trade, setTrade] = useState(price_record.gbp_trade)
	const [tradeNoVat, setTradeNoVat] = useState(price_record.gbp_trade_no_vat)

  return(
		<>
		<tr key={index} className="hover:bg-gray-50 text-gray-400 text-left">
					<td style={{'width':`${sdata.col_1}px`}} >{display_one}</td>
					<td style={{'width':`${sdata.col_2}px`}} >{display_two}</td>
					<td style={{'font-weight': 'bold', 'width':`${sdata.col_3}px`}} >£{list}</td>
					<td style={{'width':`${sdata.col_4}px`}} >£{listNoVat}</td>
					<td style={{'font-weight': 'bold', 'width':`${sdata.col_5}px`}}  >£{trade}</td>
					<td style={{'width':`${sdata.col_6}px`}}  >£{tradeNoVat}</td>
			</tr>
		</>
	)
}
