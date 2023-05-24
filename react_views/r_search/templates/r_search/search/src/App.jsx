import {useRef, useState, useEffect} from 'react'

function App() {

  const [search, setSearch] = useState('search')
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


  return (
    <div className="container px-5">
    <div className="grid grid cols-1 justify-center">
      <h1 style={{'font-size': '30px'}}>SEARCH ALL TEARSHEETS</h1>
      <p>search all tearsheets by name</p>
      <input style={{width: "300px"}} className="shadow appearance-none border rounded py-2 px-1 my-5 text-gray-700 leading-tight focus:outline-none focus:shadow-outliney-1" type='text' onChange={ (event)=> onChangeHandler(event)} value={search}></input>
      <div className="text-left py-3 text-xs">Displaying {tearsheets.length} results...</div>
      <div>
          <table className="border w-1200 text-sm text-left text-gray-500 dark:text-gray-400">
              <thead className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
              <tr>
                <th className="px-2">type</th>
                <th className="px-2">tearsheet name</th>
                <th className="px-2">updated on</th>
              </tr>
             </thead>
              <tbody>
    { is_empty ?
            <tr className="bg-white dark:bg-gray-900 dark:border-gray-700">
              <td style={{width: '150px'}} className="px-2">
               no results
              </td>
              <td style={{width: '500px'}} className="px-2  font-medium text-gray-900 whitespace-nowrap dark:text-white">
              </td>
              <td style={{width: '300px'}} className="px-2 ">
              </td>
            </tr>
    :
               tearsheets.map( (tearsheet) => { return(
                  <tr className="bg-white dark:bg-gray-900 dark:border-gray-700">
                     <td style={{width: '150px'}} className="px-2 ">
                        {tearsheet.type}
                      </td>
                      <td style={{width:'500px'}} className="px-2 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                          <a style={{'color': 'black'}} href={tearsheet.url} className="font-medium text-blue-600 dark:text-blue-500 hover:underline">{tearsheet.title}</a>
                      </td>
                      <td style={{width: '300px'}} className="px-2 ">
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
