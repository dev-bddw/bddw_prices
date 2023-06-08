import {useRef, useState, useEffect} from 'react'

function App() {

  const [search, setSearch] = useState('')
  const [filter, setFilter] = useState({'tearsheet': true, 'gbp': true,'formula': true,'gbp_formula': true })
  const [tearsheets, setTearsheets] = useState(CONTEXT.tearsheets)

  function onChangeHandler(event) {
    setSearch(event.target.value)
  }
	const isMounted = useRef(false)
	const isMountedFilter = useRef(false)
  const is_empty = tearsheets.length == 0



  // if search change, wait a moment, send data to django
  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
			if (isMounted.current) {
			  SEARCH()
			} else {
					isMounted.current = true
				}
    }, 100)
		return( () => clearTimeout(delayDebounceFn) )
  }, [search, filter])

  // function for making api call
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
			body: JSON.stringify( {'data': { search, filter } } ),
					})
						.then(response => response.json())
						.then(data => {
              setTearsheets(data.data)
							//console.log(data.data);
						})
	}

  const [print_status, setPrintStatus] = useState('None')

  // returns url for rar of all current tearsheet pdfs
  const PRINT = (tearsheets) => {
		fetch(CONTEXT.print_api, {
			credentials: 'include',
			mode: 'same-origin',
			method: "POST",
			headers: {
		    "Content-Type": "application/json",
				"Accept": 'application/json',
				'Authorization': `Token ${CONTEXT.auth_token}`,
				'X-CSRFToken': CONTEXT.csrf_token
        },
			body: JSON.stringify( {'data': { tearsheets } } ),
					})
						.then(response => response.json())
						.then(data => {
              setPrintStatus('Complete')
							console.log(data.data);
						})
	}

  function handlePrintClick() {
    setPrintStatus('Clicked')
    PRINT(tearsheets)
  }


  const return_print = () => {
    switch (print_status) {
      case 'None':
        return(
              <div className="flex content-start">
                <button className="bg-transparent text-blue-700 py-1 px-2 border border-blue-500 rounded" onClick={()=>{handlePrintClick()}}>PRINT THESE</button>
              </div>
        )
      case 'Clicked':
        return(<div role="status">
          <svg aria-hidden="true" className="inline w-8 h-8 mr-2 text-gray-200 animate-spin dark:text-gray-600 fill-gray-600 dark:fill-gray-300" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
              <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
          </svg>
          <span className="sr-only">Loading...</span>
        </div>)
      case 'Complete':
        return(<a href="">Download is ready</a>)
    }
  }

  return (
    <div className="w-full">
    <div className="grid grid cols-1 justify-center">
      <span style={{'letter-spacing':'.75rem', 'font-weight':'lighter', 'font-size':'40px'}}>SEARCH</span>
      <input style={{width: "300px"}} className="shadow appearance-none border rounded py-2 px-1 my-2 text-gray-700 leading-tight focus:outline-none focus:shadow-outliney-1" type='text' onChange={ (event)=> onChangeHandler(event)} value={search}></input>
      <FilterBox filter={filter} setFilter={setFilter}/>
      {return_print()}
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

function FilterBox({filter, setFilter}) {

  function handleChange(key) {
    //set the value for this key to its opposite
    const updated_value = { [key] : !filter[key] }
    setFilter( filter => ({
      ...filter,
      ...updated_value
    }))
  }

  return(
    <div className="py-4">
      <ul className="flex items-center">
        <li>
          <div className="pr-5">
            <input onChange={()=> handleChange('tearsheet')} checked={filter.tearsheet} className="" id="tearsheets" type="checkbox" value=""/>
            <label className="pl-2" for="tearsheets">Tearsheets</label>
          </div>
        </li>
       <li>
          <div className="px-5">
            <input onChange={()=> handleChange('gbp')} checked={filter.gbp} id="gbp" type="checkbox" value=""/>
            <label className="pl-2" for="gbp">GBP</label>
          </div>
        </li>
        <li>
          <div className="px-5">
            <input onChange={()=> handleChange('formula')} checked={filter.formula} className="ml-5" id="formula" type="checkbox" value=""/>
            <label className="pl-2" for="formula">Formula</label>
          </div>
        </li>
       <li>
          <div className="px-5">
            <input onChange={()=> handleChange('gbp_formula')} checked={filter.gbp_formula} className="ml-5" id="gbp formula" type="checkbox" value=""/>
            <label className="pl-2" for="gbp formula">Formula GBP</label>
          </div>
      </li>
   </ul>
    </div>
 )
}

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
