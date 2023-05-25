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
    <div className="container px-5">
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
                <th className="py-3 px-2">updated on</th>
              </tr>
             </thead>
              <tbody>
    { is_empty ?
            <tr className="bg-white">
              <td style={{width: '150px'}} className="px-2">
               no results
              </td>
              <td style={{width: '500px'}} className="px-2 font-medium text-gray-900 whitespace-nowrap">
              </td>
              <td style={{width: '300px'}} className="px-2 ">
              </td>
            </tr>
    :
               tearsheets.map( (tearsheet) => { return(
                  <tr className="border-b bg-white">
                     <td style={{width: '150px'}} className="py-2 px-2 ">
                        {tearsheet.type}
                      </td>
                      <td>
                        <img className="px-1 text-gray-500" style={{height:'15px'}} src={tearsheet.image}/>
                      </td>
                      <td style={{width:'500px'}} className="py-2 px-2 font-medium text-gray-500 whitespace-nowrap">
                          <a href={tearsheet.url} className="hover:underline">{tearsheet.title}</a>
                      </td>
                      <td style={{width: '300px'}} className="py-2 px-2 ">
                        {tearsheet.updated_on}
                      </td>
                  </tr>
              )} )}
             </tbody>
          </table>
      </div>
    </div>
</div>
 )
}

export default App
