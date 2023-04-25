import {useRef, useState, useEffect} from 'react';

export default function FooterDetails({footers, sdata}) {
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
				{  footers.map(  ( footer )  => { return( <FooterRow sdata={sdata} footer={footer} />)})}
			</tbody>
		</table>
		</>
	)
}

function FooterRow({sdata, footer, index}) {
	const [edit_name, setEditName] = useState(false)
  const [edit_details, setEditDetails] = useState(false)

	const [_name, setName] = useState(footer.name)
	const [_details, setDetails] = useState(footer.details)

	const isMounted = useRef(false)

	function onChangeHandler(event, setter) {
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
  }, [_name, _details])


	const CREATE = () => {
		fetch(CONTEXT.create_footer_api, {
			credentials: 'include',
			mode: 'same-origin',
			method: "POST",
			headers: {
		    "Content-Type": "application/json",
				"Accept": 'application/json',
				'Authorization': `Token ${CONTEXT.auth_token}`,
				'X-CSRFToken': CONTEXT.csrf_token
						},
			body: JSON.stringify({'data':{
				'id': footer.id,
				'name': _name,
				'details': _details
			} }),
					})
						.then(response => response.json())
						.then(data => {
							console.log(data);
						})
	}

	const UPDATE = () => {
		fetch(CONTEXT.edit_footer_api, {
			credentials: 'include',
			mode: 'same-origin',
			method: "POST",
			headers: {
		    "Content-Type": "application/json",
				"Accept": 'application/json',
				'Authorization': `Token ${CONTEXT.auth_token}`,
				'X-CSRFToken': CONTEXT.csrf_token
						},
			body: JSON.stringify({'data': {
				'id': footer.id,
				'name': _name,
				'details': _details
			} }),
					})
						.then(response => response.json())
						.then(data => {
							console.log(data);
						})
	}


	const classes="shadow appearance-none border rounded w-full py-1 text-gray-700 leading-tight focus:outline-none focus:shadow-outliney-1"

return(
				<>
					<tr className="hover:bg-gray-50 text-gray-400 text-left">
						{ edit_name ?
							<td>
								<input onChange={ (event) => onChangeHandler(event, setName)} value={_name} className={classes}></input>
							</td> :
							<td onClick={ () => { setEditName(true) } } style={{'width':`${sdata.d_col_1}%`}}>{_name}</td>
						}
						{ edit_details ?
							<td>
								<input onChange={ (event) => onChangeHandler(event, setDetails)} value={_details} className={classes}></input>
							</td> :
							<td onClick={ () => { setEditDetails(true) } } style={{'width':`${sdata.d_col_2}%`}}>{_details} </td>
						}
					</tr>
				</>
		)
	}
