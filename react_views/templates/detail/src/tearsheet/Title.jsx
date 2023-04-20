import { useState, useRef, useEffect } from 'react';
import SETTINGS from './Settings'

export default function Title({title}) {

	const links = [ {
		'name': 'VIEW PDF',
		'href': '#',
		},
		{
		'name': 'DOWNLOAD PDF',
		'href': '#',
	  },
		{
		'name': 'VIEW LIST PDF',
		'href': '#',
		},
		{
		'name': 'DOWNLOAD LIST PDF',
		'href': '#',
		},
		{
		'name': 'EDIT',
		'href': CONTEXT.edit_tearsheet,
	}]

	return (
		<div className="">
			<div className="text-gray-500 text-left">
				<a className="text-left" href="">{'<<<'} list</a>
				<span style={{'display': 'block','font-size': '30px'}} >{title}</span>
			</div>
			<div className="pb-5 text-right">
				{ links.map( (link) => { return( <><a href={link.href} className="px-1 text-gray-500 text-right">{link.name}</a>-</> )})}
			</div>
		</div>
	)
}
