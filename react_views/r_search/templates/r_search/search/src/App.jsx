import {useRef, useState, useEffect} from 'react'

function App() {

  const [search, setSearch] = useState('')
  const [tearsheets, setTearsheets] = useState(CONTEXT.tearsheets)

  function onChangeHandler(event) {
    setSearch(event.target.value)
  }
	const isMounted = useRef(false)
  const is_empty = tearsheets.length == 0

  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
			if (isMounted.current) {
			  SEARCH()
			} else {
					isMounted.current = true
				}
    }, 100)
		return( () => clearTimeout(delayDebounceFn) )
  }, [search])

	const SEARCH = () => {
		fetch(CONTEXT.search_api, {
			credentials: 'include',
			mode: 'same-origin',
			method: "POST",
			headers: {
		    "Content-Type": "application/json",
				"Accept": 'application/json',
				'Authorization': `Token ${CONTEXT.auth_token}`,
				'X-CSRFToken': CONTEXT.csrf_token
						},
			body: JSON.stringify( {'data':{ search } } ),
					})
						.then(response => response.json())
						.then(data => {
              setTearsheets(data.data)
							//console.log(data);
						})
	}

  const logo = () => {
    return(
      <img style={{height:'300px'}} className="item-center" src={CONTEXT.logo_url}/>
     )
  }

  return (
    <div className="w-full">
    <div className="grid grid cols-1 justify-center">
      <span style={{'letter-spacing':'.75rem', 'font-weight':'lighter', 'font-size':'40px'}}>SEARCH</span>
      <input style={{width: "300px"}} className="shadow appearance-none border rounded py-2 px-1 my-2 text-gray-700 leading-tight focus:outline-none focus:shadow-outliney-1" type='text' onChange={ (event)=> onChangeHandler(event)} value={search}></input>
      <div className="text-start py-3 text-gray-300 text-xs">Displaying {tearsheets.length} results...</div>
      <div className="relative overflow-x-auto shadow-md sm:rounded-lg">
          <table className="border rounded w-1200 text-sm text-left text-gray-500">
              <thead className="text-xs text-gray-400 uppercase bg-gray-50">
              <tr>
                <th className="py-3 px-2">type</th>
                <th className="py-3 px-2"></th>
                <th className="py-3 px-2"></th>
                <th className="py-3 px-2"></th>
                <th className="py-3 px-2">updated on</th>
              </tr>
             </thead>
              <tbody>
    { is_empty ?
      <tr>
          <td style={{width: '150px'}} className="py-2 px-2 ">
          </td>
          <td>
          </td>
          <td style={{width:'400px'}} className="py-2 px-2 font-medium text-gray-500 whitespace-nowrap">
          </td>
          <td style={{'font-size': '10px', width:'500px'}}>
          </td>
          <td style={{width: '300px'}} className="py-2 px-2 ">
          </td>
      </tr>
      :
               tearsheets.map( (tearsheet) => {

                 switch (tearsheet.type) {
                   case 'tearsheet':
                     return( <TearSheetRow tearsheet={tearsheet}/>)
                   case 'formula':
                     return( <TearSheetRow tearsheet={tearsheet}/>)
                   case 'gbp':
                     return( <GBPRow tearsheet={tearsheet}/>)
                   case 'formula gbp':
                     return( <GBPRow tearsheet={tearsheet}/>)
                 }
               })}
             </tbody>
          </table>
      </div>
    </div>
</div>
 )
}

export default App

function TearSheetRow({tearsheet}) {

  return(
            <tr className="border-b bg-white">
               <td style={{width: '150px'}} className="py-2 px-2 ">
                  {tearsheet.type}
                </td>
                <td>
                  <img className="px-1 text-gray-500" style={{height:'15px'}} src={tearsheet.image}/>
                </td>
                <td style={{width:'400px'}} className="py-2 px-2 font-medium text-gray-500 whitespace-nowrap">
                    <a href={tearsheet.url} className="hover:underline">{tearsheet.title}</a>
                </td>
                <td style={{'font-size': '10px', width:'500px'}}>
                 <a className="px-1" href={tearsheet.edit} style={{'display':'inline'}}>EDIT</a>
                 <a className="px-1" href={tearsheet.pdf} target='_blank' style={{'display':'inline'}}>VIEW PDF</a>
                 <a className="px-1" href={tearsheet.pdf + '?justDownload=True'} style={{'display':'inline'}}>DOWNLOAD PDF</a>
                 <a className="px-1" href={tearsheet.pdf_list} target='_blank' style={{'display':'inline'}}>VIEW LIST PDF</a>
                 <a className="px-1" href={tearsheet.pdf_list + '?justDownload=True'} style={{'display':'inline'}}>DOWNLOAD PDF</a>
                </td>
                <td style={{width: '300px'}} className="py-2 px-2 ">
                  {tearsheet.updated_on}
                </td>
            </tr>

  )
}


function GBPRow({tearsheet}) {

  return(
            <tr className="border-b bg-white">
               <td style={{width: '150px'}} className="py-2 px-2 ">
                  {tearsheet.type}
                </td>
                <td>
                  <img className="px-1 text-gray-500" style={{height:'15px'}} src={tearsheet.image}/>
                </td>
                <td style={{width:'400px'}} className="py-2 px-2 font-medium text-gray-500 whitespace-nowrap">
                    <a href={tearsheet.url} className="hover:underline">{tearsheet.title}</a>
                </td>
                <td style={{'font-size': '10px', width:'500px'}}>
                 <a className="px-1" href={tearsheet.edit} style={{'display':'inline'}}>EDIT</a>
                 <a className="px-1" href={tearsheet.pdf} target='_blank' style={{'display':'inline'}}>VIEW PDF</a>
                 <a className="px-1" href={tearsheet.pdf + '?justDownload=True'} style={{'display':'inline'}}>DOWNLOAD PDF</a>
                 <a className="px-1" href={tearsheet.pdf_list} target='_blank' style={{'display':'inline'}}>VIEW TRADE PDF</a>
                 <a className="px-1" href={tearsheet.pdf_list + '?justDownload=True'} style={{'display':'inline'}}>DOWNLOAD TRADE PDF</a>
                </td>
                <td style={{width: '300px'}} className="py-2 px-2 ">
                  {tearsheet.updated_on}
                </td>
            </tr>

  )
}
