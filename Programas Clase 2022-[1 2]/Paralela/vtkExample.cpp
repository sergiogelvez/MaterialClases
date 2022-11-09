struct integrator_rk4
{
    float3 p; // position
    float  t; // time

    template<typename Field>
    void __device__ step( const Field& field, const float dt ) 
    {
        
        if( isnan(t) )
            return;

        const float dt_half = 0.5 * dt;

        float3 k1, k2, k3, k4;

        if( !field.get( p, k1 ) )
            goto outside;

        if( !field.get( p + dt_half*k1, k2 ) )
            goto outside;

        if( !field.get( p + dt_half*k2, k3 ) )
            goto outside;

        if( !field.get( p + dt * k3, k4 ) )
            goto outside;
            
        p += dt / 6.0f * (k1 + k2 + k3 + k4);
        t += dt;

        return;

    outside:
        t = nanf(0);
    }
};

void save_as_vtk( thrust::host_vector<integrator_rk4> houtput, 
                  unsigned int num_seeds, 
                  unsigned int num_steps, 
                  const std::string& filename ) 
{
    std::vector<int>   offset, connectivity;
    std::vector<float> coord, itime;

    unsigned int num_points = 0;

    // unpack all the streamline points into separate arrays
    // (discarding any invalid points)
    auto iter = houtput.begin();

    for( unsigned int seed=0; seed<num_seeds; ++seed, ++iter )
    {
        offset.push_back( connectivity.size() );

        auto iiter = iter;

        for( unsigned int step=0; step<num_steps; ++step, iiter += num_seeds )
        {
            auto& si = *iiter;

            if( isnan( si.t ) )
                break;

            coord.push_back( si.p.x );
            coord.push_back( si.p.y );
            coord.push_back( si.p.z );
            itime.push_back( si.t );

            connectivity.push_back( num_points );

            ++num_points;
        }
    }

    // write to VTP file
    std::ofstream out( filename );

    out << "<?xml version=\"1.0\"?>\n"
        << "<VTKFile type=\"PolyData\" version=\"0.1\" byte_order=\"LittleEndian\">"
        << "<PolyData>"
        << "<Piece "
            << "NumberOfPoints=\"" << num_points << "\" " 
            << "NumberOfVerts=\"0\" "
            << "NumberOfLines=\"" << num_seeds << "\" "
            << "NumberOfStris=\"0\" "
            << "NumberOfPolys=\"0\">"
        << "<Points>"
        << "<DataArray "
            << "type=\"Float32\" "
            << "NumberOfComponents=\"3\" "
            << "format=\"ascii\">\n";

    for( auto c : coord )
        out << c << ' ';

    out << "</DataArray>"
        << "</Points>";

    out << "<Lines>"
        << "<DataArray Name=\"connectivity\" "
            << "type=\"Int32\" format=\"ascii\">\n";
    
    for( auto c : connectivity )
        out << c << '\n';
    
    out << "</DataArray>"
        << "<DataArray Name=\"offsets\" "
            << "type=\"Int32\" format=\"ascii\">\n";
    
    for( auto o : offset )
        out << o << '\n';

    out << "</DataArray>"
        << "</Lines>"
        << "<PointData Scalars=\"time\">"
        << "<DataArray Name=\"time\" type=\"Float32\" format=\"ascii\">\n";
    
    for( auto t : itime )
        out << t << '\n';

    out << "\n</DataArray>"
        << "</PointData>"
        << "</Piece>"
        << "</PolyData>"
        << "</VTKFile>"
        << '\n';

    std::cerr << "wrote " << num_seeds << " streamlines ("
              << num_points << " points) to "
              << filename << '\n';
}

// -------------------------------------------------------------------------



/* thrust::host_vector<integrator_rk4> houtput( num_steps * num_seeds );
save_as_vtk( houtput, num_seeds, num_steps, "test.vtp" ); */