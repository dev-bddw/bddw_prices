import {useRef, useState, useEffect} from 'react';
import SETTINGS from './Settings'

function Details({details, sdata}) {
	return(
    <>
			<div style={{'height': sdata.pt}}/>
	  <table style={{'width': '850px'}} className="mx-auto table-auto">
	  	<thead className="text-gray-400 text-left">
				<th></th>
				<th></th>
				<th></th>
				<th></th>
				<th></th>
			</thead>
			<tbody>
				{  details.map(  ( obj )  => { return( Object.entries(obj).map( ([key, value]) => { return( <DetailGroup sdata={sdata} details={value} name={key} />)}))})}
			</tbody>
		</table>
		</>
	)
}

export default Details;


function DetailGroup ({sdata, details, name}) {

	return(
		<>
			{ details.map( (detail, index) => {
				return(
					<DetailRow sdata={sdata} detail={detail} name={name} index={index}/>
					)
			})}
		</>
	)
}


function DetailRow({sdata, detail, name, index}) {

return(
				<>
					<tr className="hover:bg-gray-50 text-gray-400 text-left">
							<td style={{'width':`${sdata.d_col_1}%`}}> { index == 0 ? detail.name : null} </td>
							<td style={{'width':`${sdata.d_col_2}%`}}>{detail.details} </td>
					</tr>
				</>
		)
	}
