import { useState, useRef, useEffect } from 'react';
import SETTINGS from './Settings'

function Captions({captions, sdata}) {

	return(

		<>
			<div style={{'height': sdata.pt}}/>
		<table style={{'width': '850px'}} className="py-5 mx-auto table-auto">
							<thead className="text-gray-400 text-left">
									<th></th>
									<th></th>
									<th></th>
									<th></th>
									<th></th>
							</thead>
							<tbody>
								{ captions.map( (caption, index) => {
									return(<Caption sdata={sdata} caption={caption} index={index}/>)})}
							</tbody>
						</table>
		</>
	)
}

export default Captions;

function Caption({caption, sdata, index}) {

return(
		<>
					<tr className="hover:bg-gray-50 text-gray-400 text-left">
							<td style={{'width':`${sdata.d_col_1}%`}}> { caption.caption_title } </td>
							<td style={{'width':`${sdata.d_col_2}%`}}> { caption.caption } </td>
					</tr>
				</>
		)
}
