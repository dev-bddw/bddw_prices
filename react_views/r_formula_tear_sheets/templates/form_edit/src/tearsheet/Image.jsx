import { useState, useRef, useEffect } from 'react';

export default function Image({img }) {

	const [ img_url, setImgUrl] = useState(img)
	const [ img_data, setImgData] = useState()
	const isMounted = useRef(false)
	const hiddenFileInput = useRef(null)

	function handleClick(event) {
		// use refs to programmatically use default behavior https://blog.logrocket.com/complete-guide-react-refs/
		hiddenFileInput.current.click();
	}

	function onChangeHandler(event) {
		setImgData(event.target.files[0])
	}


	// add a delay, then execute the api call on cleanup
  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
			if (isMounted.current) {
			  POST()
			} else {
					isMounted.current = true
				}
    }, 1500)
		return( () => clearTimeout(delayDebounceFn) )
  }, [img_data])


	const POST = () => {

		let form_data = new FormData();
		form_data.append('image', img_data)

		fetch(CONTEXT.edit_image_api, {
			credentials: 'include',
			mode: 'same-origin',
			method: "POST",
			headers: {
				'Authorization': `Token ${CONTEXT.auth_token}`,
				'X-CSRFToken': CONTEXT.csrf_token
						},
			body: form_data
					})
						.then(response => response.json())
						.then(data => { setImgUrl(data.url) } )
	}

	return (
		<div>
				<div onClick={ (event) => { handleClick(event)}} className="cursor-pointer relative">
					<img className='hover:opacity-90 object-fill' src={img_url}/>
					<input style={{'display': 'none'}} ref={hiddenFileInput} type="file" name="image_url" accept="image/jpeg,image/png,image/gif" onChange={(event) => {onChangeHandler(event)}}></input>
					<p className="opacity-25 hover:opacity-100 duration-300 absolute text-5xl underline text-white top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">Change Image</p>
				</div>
		</div>
	)
}
