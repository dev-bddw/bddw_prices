import { processContext, categoryOrder } from './utils/Process';
import {useState } from 'react';

function App() {

  const [pricelist, setPriceList] = useState(processContext(CONTEXT.pricelist))
  const [categories, setCategories] = useState(Object.keys(categoryOrder))
  const [gbp, setGbp] = useState(true)


  return (
    <div>
      <div style={{'width':'50px','font-size': '7px'}}>
        {categories.map( (category)=> {
          return(<p><a href={'#' + category}>{category}</a></p>)
        })}
      </div>
      <div>
            {pricelist.map( (series_item, index, self)=> {
              return(<SeriesItemTable _all={self} gbp={gbp} index={index} series_item={series_item}/>
              )})}
      </div>
    </div>
 )
}

export default App

function SeriesItemTable( {gbp, series_item, index, _all} ) {

  function handleCategoryDisplay() {
      if (index == 0) {
        return( <p style={{'font-size': '25px'}} id={series_item.category}>{series_item.category}</p>)
      } else if (index != 0) {
        return( (series_item.category != _all[index - 1].category ? <p style={{'font-size': '25px'}} id={series_item.category}>{series_item.category}</p> : null ) )
      }
    }

  return(

      <div key={index} className="py-2 relative overflow-x-auto">
      {handleCategoryDisplay()}
      { gbp ?
       <table style={{'font-size': '8px'}} className="w-full w-1200 text-left text-gray-500">
            <thead className="border-b border-gray-900">
            <tr>
              <th style={{'width': '20%'}} className="text-gray-200 px-2"></th>
              <th style={{'width': '5%'}} className="px-2"></th>
              <th style={{'width': '25%'}} className="px-2"></th>
              <th style={{'width': '10%'}} className="px-2">LIST</th>
              <th style={{'width': '10%'}} className="px-2"></th>
              <th style={{'width': '10%'}} className="px-2">TRADE</th>
              <th style={{'width': '10%'}} className="px-2"></th>
            </tr>
           </thead>
            <tbody>
            <tr style={{'font-size': '8px'}} className="border-b bg-white hover:bg-gray-200">
                <td className="px-2">{series_item.series_item}</td>
                <td className="px-2"></td>
                <td className="px-2"></td>
                <td className="px-2">INC VAT</td>
                <td className="px-2">EXC VAT</td>
                <td className="px-2">INC VAT</td>
                <td className="px-2">EXC VAT</td>
              </tr>

              { series_item.price_records.map( (pr, index) => {
                return(
                  <GBPRow priceRecord={pr} index={index} />
                  )}
                )
              }
           </tbody>
        </table>
          :
       <table style={{'font-size': '8px'}} className="w-full w-1200 text-left text-gray-500">
            <thead className="border-b border-gray-900">
            <tr>
              <th style={{'width': '25%'}} className="text-gray-200 px-2"></th>
              <th style={{'width': '5%'}} className="px-2"></th>
              <th style={{'width': '25%'}} className="px-2"></th>
              <th style={{'width': '5%'}} className="px-2">LIST</th>
              <th style={{'width': '5%'}} className="px-2">NET</th>
            </tr>
           </thead>
            <tbody>
              { series_item.price_records.map( (pr, index) => {
                return(
                  <Row priceRecord={pr} index={index} />
                  )}
                )
              }
           </tbody>
        </table>
      }
    </div>
  )
}

function GBPRow({priceRecord, index }) {
  return(
    <tr key={priceRecord.id} className="border-b bg-white hover:bg-gray-200">
      <td className="px-2"></td>
      <td className="px-2">{priceRecord.rule_type}</td>
      <td className="px-2 text-end">{priceRecord.rule_display_1} {priceRecord.rule_display_2}</td>
      <td className="px-2">£{priceRecord.gbp_price}</td>
      <td className="px-2">£{priceRecord.gbp_price_no_vat}</td>
      <td className="px-2">£{priceRecord.gbp_trade}</td>
      <td className="px-2">£{priceRecord.gbp_trade_no_vat}</td>
    </tr>
  )
}

function Row({priceRecord, index }) {
  return(
    <tr key={priceRecord.id} className="border-b bg-white hover:bg-gray-200">
      <td className="px-2">{ (index == 0) ? priceRecord.series_item : null}</td>
      <td className="px-2">{priceRecord.rule_type}</td>
      <td className="px-2 text-end">{priceRecord.rule_display_1} {priceRecord.rule_display_2}</td>
      <td className="px-2">${priceRecord.list_price}</td>
      <td className="px-2">${priceRecord.net_price}</td>
    </tr>
  )
}
