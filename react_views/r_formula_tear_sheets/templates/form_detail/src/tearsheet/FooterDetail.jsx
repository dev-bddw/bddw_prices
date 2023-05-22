import {useRef, useState, useEffect} from 'react';

export default function FooterDetails({footers, sdata}) {
	return(
    <>
			<div style={{'height': sdata.pt_footer}}/>
	  <table className="table-auto">
	  	<thead className="text-gray-400 text-left">
				<th></th>
				<th></th>
				<th></th>
				<th></th>
				<th></th>
			</thead>
			<tbody>
				{  footers.map(  ( footer )  => { return( <FooterRow sdata={sdata} footer={footer} />)})}
			</tbody>
		</table>
		</>
	)
}

function FooterRow({sdata, footer, index}) {

	const [_name, setName] = useState(footer.name)
	const [_details, setDetails] = useState(footer.details)

	const isMounted = useRef(false)

return(
				<>
					<tr className="hover:bg-gray-50 text-gray-400 text-left">
							<td style={{'width':`${sdata.d_col_1}px`}}>{_name}</td>
							<td style={{'width':`${sdata.d_col_2}px`}}>{_details} </td>
					</tr>
				</>
		)
	}
