import open3d
import numpy as np
import plotly.graph_objects as go

def visualization_draw_geometry(pcd, background='black'):
    vis = open3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(pcd)
    if background=='black':
        vis.get_render_option().background_color = np.asarray([0, 0, 0])
    elif background=='white':
        vis.get_render_option().background_color = np.asarray([1, 1, 1])
    else:
        print("Wrong background chosen! Choose either 'white' OR 'black'.")
    vis.run()
    vis.destroy_window()



def plotly_distance(points, show=True):
    # Calculate distances from the origin
    distances = np.linalg.norm(points, axis=1)

    # Create the 3D scatter plot
    fig = go.Figure(data=[go.Scatter3d(
        x=points[:, 0],
        y=points[:, 1],
        z=points[:, 2],
        mode='markers',
        marker=dict(
            size=2,
            color=distances,  # use distances for color
            colorscale='Inferno',  # choose a colorscale
            colorbar=dict(title="Distance from Origin"),  # add a colorbar title
            opacity=0.8
        )
    )])
    fig.update_scenes(aspectmode='data')

    if show == True:
        fig.show()


def visualization_draw_geometry_list(pcd_list):
    vis = open3d.visualization.Visualizer()
    vis.create_window()

    for pcd in pcd_list:
        vis.add_geometry(pcd)

    vis.get_render_option().background_color = np.asarray([1, 1, 1])
    vis.run()
    vis.destroy_window()

    def mode_plotly(point_cloud, mode='reflectance'):
        # Extract the point cloud's coordinates as a numpy array
        points = np.asarray(point_cloud.points)

        # Calculate distances from the origin
        distances = np.linalg.norm(points, axis=1)

        # Check if the point cloud has color information
        if hasattr(point_cloud, 'colors') and len(point_cloud.colors) == len(point_cloud.points):
            colors = np.asarray(point_cloud.colors)
            color_values = distances
        else:
            colors = np.zeros((len(point_cloud.points), 3))  # Default to black color if no colors provided

        if mode == 'reflectance':
            fig = go.Figure(data=[go.Scatter3d(
                x=points[:, 0],
                y=points[:, 1],
                z=points[:, 2],
                mode='markers',
                marker=dict(
                    size=2,
                    color=colors,
                    opacity=0.8
                )
            )])

        elif mode == 'distance':
            fig = go.Figure(data=[go.Scatter3d(
                x=points[:, 0],
                y=points[:, 1],
                z=points[:, 2],
                mode='markers',
                marker=dict(
                    size=2,
                    color=color_values,  # use color_values for color
                    colorscale='Inferno',  # choose a colorscale
                    colorbar=dict(title="Color Value"),  # add a colorbar title
                    opacity=0.8
                )
            )])

        else:
            print("Wrong mode chosen! Choose either: 'reflectance' OR 'distance'!")

        # Update the scene layout if needed
        fig.update_layout(
            scene=dict(
                xaxis=dict(visible=False, range=[-70, 70]),
                yaxis=dict(visible=False, range=[-40, 40]),
                zaxis=dict(visible=False, range=[-5, 1]),
                aspectmode='manual', aspectratio=dict(x=2, y=1, z=0.1),
                camera=dict(
                    up=dict(x=0.15, y=0, z=1),
                    center=dict(x=0, y=0, z=0.1),
                    eye=dict(x=-0.3, y=0, z=0.2)
                )
            ),
            # plot_bgcolor='black', #background
            # paper_bgcolor='black', #background
            scene_dragmode='orbit'
        )

        return fig


def visualize_reflectance_distance(point_cloud, mode, save=False, show=True, output_folder='output',
                                   filename='processed'):
    """
    Visualize a 3D point cloud and optionally save the plot as an image.

    Parameters:
        point_cloud (numpy.ndarray): The 3D point cloud data.
        save (bool, optional): If True, the plot will be saved as an image. Default is False.
        show (bool, optional): If True, the plot will be displayed interactively. Default is True.
        output_folder (str, optional): The folder where the image will be saved. Default is 'output'.
        filename (str, optional): The name of the saved image file. Default is 'processed'.

    Returns:
        plotly.graph_objects.Figure: The Plotly figure object.
    """
    # Call get_plotly_fig with the provided point cloud and other parameters to get the Plotly figure
    fig = mode_plotly(point_cloud, mode=mode)

    if show:
        fig.show()

    # Save the plot as an image if save is True
    if save:
        image_path = f"{output_folder}/{filename}_processed.jpg"
        fig.write_image(image_path, scale=3)
        print(f"Plot saved as: {image_path}")

    return fig


def plotly_fig(point_cloud):
    # Extract the point cloud's coordinates as a numpy array
    points = np.asarray(point_cloud.points)

    # Check if the point cloud has color information
    if hasattr(point_cloud, 'colors') and len(point_cloud.colors) == len(point_cloud.points):
        colors = np.asarray(point_cloud.colors)
    else:
        colors = np.zeros((len(point_cloud.points), 3))  # Default to black color if no colors provided

    fig = go.Figure(data=[go.Scatter3d(
        x=points[:, 0],
        y=points[:, 1],
        z=points[:, 2],
        mode='markers',
        marker=dict(
            size=2,
            color=colors,
            opacity=0.8
        )
    )])

    # Update the scene layout if needed
    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False, range=[-70, 70]),
            yaxis=dict(visible=False, range=[-40, 40]),
            zaxis=dict(visible=False, range=[-5, 1]),
            aspectmode='manual', aspectratio=dict(x=2, y=1, z=0.1),
            camera=dict(
                up=dict(x=0.15, y=0, z=1),
                center=dict(x=0, y=0, z=0.1),
                eye=dict(x=-0.3, y=0, z=0.2)
            )
        ),
        plot_bgcolor='black',  # background
        paper_bgcolor='black',  # background
        scene_dragmode='orbit'
    )

    return fig


def visualize_point_clouds(*point_clouds, show=True, save=False, output_folder='output', filename='combined'):
    """
    Visualize one or more 3D point clouds and optionally save the plot as an image.

    Parameters:
        *point_clouds: Variable-length arguments, each representing a 3D point cloud data.
                       Can be numpy.ndarray or open3d.geometry.PointCloud.
        show (bool, optional): If True, the plot will be displayed interactively. Default is True.

    Returns:
        plotly.graph_objects.Figure: The Plotly figure object.
    """
    fig_combined = go.Figure()

    for pc in point_clouds:
        # Convert input to Open3D PointCloud if provided as a numpy array
        if isinstance(pc, np.ndarray):
            pc = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(pc))

        # Call get_plotly_fig to get the Plotly figure for the current point cloud
        fig = plotly_fig(pc)

        # Add the trace from the current figure to the combined figure
        fig_combined.add_trace(fig.data[0])

    # Update the layout if needed (common for all point clouds)
    fig_combined.update_layout(fig.layout)

    if show:
        fig_combined.show()

    # Save the plot as an image if save is True
    if save:
        print("\nSaving...")
        image_path = f"{output_folder}/{filename}_combined.jpg"
        fig_combined.write_image(image_path, scale=1)
        print(f"Plot saved as: {image_path}")

    return fig_combined


### ------------ LANE DETECTION ------------------- ###


def reflectivity_threshold(point_cloud, threshold=0.5):
    """
    Filters a point cloud based on reflectivity threshold.

    Parameters:
        pcd (open3d.geometry.PointCloud): The input point cloud.
        threshold (float, optional): The reflectivity threshold. Points with reflectivity above this value will be kept.
            Default is 0.5.

    Returns:
        open3d.geometry.PointCloud: A new point cloud with points whose reflectivity is above the threshold.
    """
    if not hasattr(point_cloud, 'colors'):
        # If colors (reflectivity information) are not available, return the original point cloud
        return point_cloud

    # Get the reflectivity values (assuming reflectivity is stored in the red channel of the colors)
    colors = np.asarray(point_cloud.colors)
    reflectivities = colors[:, 0]

    # Create a mask of points that have reflectivity above the threshold
    mask = reflectivities > threshold

    # Filter points and reflectivities using the mask
    filtered_points = np.asarray(point_cloud.points)[mask]
    filtered_colors = colors[mask]

    # Create a new point cloud with the filtered points and colors
    filtered_point_cloud = o3d.geometry.PointCloud()
    filtered_point_cloud.points = o3d.utility.Vector3dVector(filtered_points)
    filtered_point_cloud.colors = o3d.utility.Vector3dVector(filtered_colors)

    return filtered_point_cloud


def roi_filter(pcd, roi_min=(0, -3, -2), roi_max=(20, 3, 0)):
    """
    Filters a point cloud based on a region of interest (ROI) defined by the minimum and maximum coordinates.

    Parameters:
        pcd (open3d.geometry.PointCloud): The input point cloud.
        roi_min (tuple, optional): The minimum (x, y, z) coordinates of the ROI. Default is (0, -3, -2).
        roi_max (tuple, optional): The maximum (x, y, z) coordinates of the ROI. Default is (20, 3, 0).

    Returns:
        open3d.geometry.PointCloud: A new point cloud containing points within the specified ROI.
    """
    # Convert the point cloud points to a numpy array
    points = np.asarray(pcd.points)

    # Create a mask for points that fall within the ROI
    mask_roi = np.logical_and.reduce((
        points[:, 0] >= roi_min[0],
        points[:, 0] <= roi_max[0],
        points[:, 1] >= roi_min[1],
        points[:, 1] <= roi_max[1],
        points[:, 2] >= roi_min[2],
        points[:, 2] <= roi_max[2]
    ))

    # Filter points using the mask
    roi_points = points[mask_roi]

    # Create a new point cloud with the filtered points
    roi_pcd = o3d.geometry.PointCloud()
    roi_pcd.points = o3d.utility.Vector3dVector(roi_points)

    return roi_pcd


def lane_line_detection(point_cloud):
    point_cloud_copy = copy.deepcopy(point_cloud)
    print(point_cloud_copy)
    # Thresholding
    filtered_point_cloud = reflectivity_threshold(point_cloud_copy, threshold=0.45)
    print(filtered_point_cloud)

    # Region of Interest
    roi_point_cloud = roi_filter(filtered_point_cloud, roi_min=(0, -3, -2), roi_max=(20, 3, 0))
    print(roi_point_cloud)

    return roi_point_cloud


def ransac(point_cloud, distance_threshold=0.33, ransac_n=3, num_iterations=100):
    """
    RANSAC-based plane segmentation for a point cloud.

    Parameters:
        point_cloud (open3d.geometry.PointCloud): The input point cloud.
        distance_threshold (float, optional): The maximum distance a point can be from the plane to be considered an inlier.
            Default is 0.33.
        ransac_n (int, optional): The number of points to randomly sample for each iteration of RANSAC. Default is 3.
        num_iterations (int, optional): The number of RANSAC iterations to perform. Default is 100.

    Returns:
        open3d.geometry.PointCloud, open3d.geometry.PointCloud: Two point clouds representing the inliers and outliers
        of the segmented plane, respectively.
    """
    # Perform plane segmentation using RANSAC
    plane_model, inliers = point_cloud.segment_plane(distance_threshold=distance_threshold, ransac_n=ransac_n,
                                                     num_iterations=num_iterations)

    # Extract inlier and outlier point clouds
    inlier_cloud = point_cloud.select_by_index(inliers)
    outlier_cloud = point_cloud.select_by_index(inliers, invert=True)

    # Color the outlier cloud red and the inlier cloud blue
    outlier_cloud.paint_uniform_color([0.8, 0.2, 0.2])  # Red
    inlier_cloud.paint_uniform_color([0.25, 0.5, 0.75])  # Blue

    return outlier_cloud, inlier_cloud


def dbscan(outlier_cloud, eps=1.0, min_points=10):
    labels = np.array(outlier_cloud.cluster_dbscan(eps=eps, min_points=min_points, print_progress=True))
    max_label = labels.max()
    print(f"\npoint cloud has {max_label + 1} clusters")
    colors = plt.get_cmap("inferno_r")(labels / (max_label if max_label > 0 else 1))
    colors[labels < 0] = 0
    outlier_cloud.colors = open3d.utility.Vector3dVector(colors[:, :3])
    return outlier_cloud, labels


def get_bounding_boxes(labels, outlier_cloud, MAX_POINTS=300):
    """
    Get axis-aligned bounding boxes (boxes) for clusters in a point cloud.

    Parameters:
        labels (numpy.ndarray): The cluster labels assigned to each point in the point cloud.
        outlier_cloud (open3d.geometry.PointCloud): The point cloud containing the outlier points.

    Returns:
        list of open3d.geometry.OrientedBoundingBox: A list of axis-aligned bounding boxes (boxes) for each cluster.
    """
    # Extract points for each cluster
    clusters = {}
    for i, label in enumerate(labels):
        if label >= 0:
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(outlier_cloud.points[i])

    # Filter out clusters with more than 300 points (optional)
    clusters = {label: points for label, points in clusters.items() if len(points) <= MAX_POINTS}

    # Create boxes for each cluster
    boxes = []
    for points in clusters.values():
        cluster_cloud = o3d.geometry.PointCloud()
        cluster_cloud.points = o3d.utility.Vector3dVector(points)
        aabb = cluster_cloud.get_axis_aligned_bounding_box()  # PCA
        boxes.append(aabb)
    return boxes


def pca(labels, outlier_cloud, inlier_cloud, MAX_POINTS, MIN_POINTS):
    """
    Perform PCA (Principal Component Analysis) on the point cloud clusters.

    Parameters:
        outlier_cloud (open3d.geometry.PointCloud): The point cloud containing the outlier points.
        inlier_cloud (open3d.geometry.PointCloud): The point cloud containing the inlier points.
        MAX_POINTS (int): The maximum number of points in a cluster to consider for PCA.
        MIN_POINTS (int): The minimum number of points in a cluster to consider for PCA.

    Returns:
        list of open3d.geometry.OrientedBoundingBox: A list of oriented bounding boxes (OBB) for each cluster.
    """
    obs = []
    # Group points by cluster label
    indexes = pd.Series(range(len(labels))).groupby(labels, sort=False).apply(list).tolist()

    # Iterate over clusters and perform PCA
    for i in range(0, len(indexes)):
        nb_points = len(outlier_cloud.select_by_index(indexes[i]).points)
        if nb_points > MIN_POINTS and nb_points < MAX_POINTS:
            sub_cloud = outlier_cloud.select_by_index(indexes[i])
            obb = sub_cloud.get_oriented_bounding_box()
            obb.color = (1, 1, 0)  # Set color of the oriented bounding box to yellow (1, 1, 0)
            obs.append(obb)

    # Combine the outlier cloud, PCA bounding boxes, and inlier cloud in a list
    list_of_visuals = []
    list_of_visuals.append(outlier_cloud)
    list_of_visuals.extend(obs)
    list_of_visuals.append(inlier_cloud)
    return list_of_visuals


def get_trace(obb_boxes, fig):
    for obb in obb_boxes:
        # Get the eight corner points of the OBB
        corners = np.asarray(obb.get_box_points())

        # Extract x, y, and z coordinates of the corners
        x = corners[:, 0]
        y = corners[:, 1]
        z = corners[:, 2]
        # Create a Mesh3d trace for the oriented bounding box with opacity
        obb_trace = go.Mesh3d(
            x=x,
            y=y,
            z=z,
            i=[0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 4, 5, 6, 7, 0, 2, 6, 4, 1, 3, 7, 5],
            j=[1, 2, 3, 0, 5, 6, 7, 4, 2, 3, 7, 6, 1, 0, 4, 5, 6, 7, 3, 2, 0, 1, 5, 4],
            k=[2, 3, 0, 1, 6, 7, 4, 5, 3, 7, 6, 2, 0, 4, 5, 1, 7, 6, 2, 4, 1, 5, 0, 3],
            color='blue',
            opacity=0.3
        )

        # Add the Mesh3d trace to the figure
        fig.add_trace(obb_trace)
    return fig
