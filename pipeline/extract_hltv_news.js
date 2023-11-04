const fs = require('fs')
const path = require('path')
const { HLTV } = require('hltv')

const dataDirectory = path.join(__dirname)

if (!fs.existsSync(dataDirectory)) {
    fs.mkdirSync(dataDirectory)
}

const today = new Date()
const year = today.getFullYear()
const month = today.toLocaleString('default', { month: 'long' }).toLowerCase()

const newsFilePath = path.join(dataDirectory, 'news.json')
const errorFilePath = path.join(dataDirectory, 'error.json')

HLTV.getNews({ 'year': year, 'month': month })
    .then((res) => {
        fs.writeFileSync(newsFilePath, JSON.stringify(res, null, 2))
        console.log('News data saved to news.json')
    })
    .catch((err) => {
        fs.writeFileSync(errorFilePath, JSON.stringify(err, null, 2))
        console.error('Error data saved to error.json')
    })

