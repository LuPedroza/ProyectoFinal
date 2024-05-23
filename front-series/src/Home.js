import React, { useState, useEffect } from 'react';
import './App.css';
import Card from 'react-bootstrap/Card';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Pagination from 'react-bootstrap/Pagination';

const ITEMS_PER_PAGE = 12;

function Home() {
  const [series, setSeries] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);

  useEffect(() => {
    fetch('http://localhost:8000/series/?tipo=todas')
      .then(response => response.json())
      .then(data => setSeries(data))
      .catch(error => console.error('Error fetching series:', error));
  }, []);

  const handlePageChange = (pageNumber) => {
    setCurrentPage(pageNumber);
  };

  // Calculate the index range for the current page
  const indexOfLastItem = currentPage * ITEMS_PER_PAGE;
  const indexOfFirstItem = indexOfLastItem - ITEMS_PER_PAGE;
  const currentItems = series.slice(indexOfFirstItem, indexOfLastItem);

  // Calculate total pages
  const totalPages = Math.ceil(series.length / ITEMS_PER_PAGE);

  // Generate pagination items
  const renderPaginationItems = () => {
    let items = [];

    if (currentPage > 1) {
      items.push(
        <Pagination.Prev key="prev" onClick={() => handlePageChange(currentPage - 1)} />
      );
    }

    for (let number = 1; number <= totalPages; number++) {
      if (number === currentPage || number === currentPage - 1 || number === currentPage + 1 || number === 1 || number === totalPages) {
        items.push(
          <Pagination.Item
            key={number}
            active={number === currentPage}
            onClick={() => handlePageChange(number)}
          >
            {number}
          </Pagination.Item>
        );
      } else if (number === 2 && currentPage > 3) {
        items.push(<Pagination.Ellipsis key="start-ellipsis" />);
      } else if (number === totalPages - 1 && currentPage < totalPages - 2) {
        items.push(<Pagination.Ellipsis key="end-ellipsis" />);
      }
    }

    if (currentPage < totalPages) {
      items.push(
        <Pagination.Next key="next" onClick={() => handlePageChange(currentPage + 1)} />
      );
    }

    return items;
  };

  return (
    <Container>
      <Encabezado />
      <br />
      <Row className="card-container">
        {currentItems.map(serie => (
          <Col key={serie.NombreSerie} xs={12} sm={6} md={4} lg={3} className="mb-4">
            <CardL serie={serie} />
          </Col>
        ))}
      </Row>
      <Pagination className="pagination-custom justify-content-center mt-4">
        {renderPaginationItems()}
      </Pagination>
    </Container>
  );
}

function Encabezado() {
  return (
    <div>
      <br />
      <div className="row" style={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-start' }}>
        <div className="col-md-5" style={{ textAlign: 'right' }}>
          <img
            src="https://www.animaker.es/blog/wp-content/uploads/2023/08/New_Courage-271x300.webp"
            alt="Courage the Cowardly Dog"
            style={{ maxWidth: '100px', height: 'auto', marginRight: '0px' }}
          />
        </div>
        <div className="col-md-7" style={{ textAlign: 'left' }}>
          <h1 className="titulo">
            ToonMania
          </h1>
        </div>
      </div>
    </div>
  );
}

function CardL({ serie }) {
  return (
    <Card style={{ width: '15rem', height: '27rem', margin: '10px' }}>
      <Card.Img variant="top" src={serie.imagen} style={{ height: '9rem' }} />
      <Card.Body>
        <Card.Title style={{ fontSize: '0.9rem' }}>{serie.NombreSerie}</Card.Title>
        <Card.Text style={{ fontSize: '0.8rem' }}>
          Calificación Google: {serie.calificacionGoogle} <br />
          Calificación IBM: {serie.calificacionIBM} <br />
          Descripción: {serie.Descripcion} <br />
          Número de Episodios: {serie.numeroEpisodios} <br />
          Canal: {serie.NombreCanal} <br />
          Audiencia: {serie.NombreAudiencia} <br />
          Técnicas: {serie.Tecnicas} 
        </Card.Text>
      </Card.Body>
    </Card>
  );
}

export default Home;
