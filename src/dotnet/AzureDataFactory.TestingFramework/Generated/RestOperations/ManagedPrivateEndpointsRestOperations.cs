// <auto-generated/>

#nullable disable

using System.Text.Json;
using Azure.Core;
using Azure.Core.Pipeline;
using AzureDataFactory.TestingFramework.Models;

namespace Azure.ResourceManager.DataFactory
{
    internal partial class ManagedPrivateEndpointsRestOperations
    {
        private readonly TelemetryDetails _userAgent;
        private readonly HttpPipeline _pipeline;
        private readonly Uri _endpoint;
        private readonly string _apiVersion;

        /// <summary> Initializes a new instance of ManagedPrivateEndpointsRestOperations. </summary>
        /// <param name="pipeline"> The HTTP pipeline for sending and receiving REST requests and responses. </param>
        /// <param name="applicationId"> The application id to use for user agent. </param>
        /// <param name="endpoint"> server parameter. </param>
        /// <param name="apiVersion"> Api Version. </param>
        /// <exception cref="ArgumentNullException"> <paramref name="pipeline"/> or <paramref name="apiVersion"/> is null. </exception>
        public ManagedPrivateEndpointsRestOperations(HttpPipeline pipeline, string applicationId, Uri endpoint = null, string apiVersion = default)
        {
            _pipeline = pipeline ?? throw new ArgumentNullException(nameof(pipeline));
            _endpoint = endpoint ?? new Uri("https://management.azure.com");
            _apiVersion = apiVersion ?? "2018-06-01";
            _userAgent = new TelemetryDetails(GetType().Assembly, applicationId);
        }

        internal HttpMessage CreateListByFactoryRequest(string subscriptionId, string resourceGroupName, string factoryName, string managedVirtualNetworkName)
        {
            var message = _pipeline.CreateMessage();
            var request = message.Request;
            request.Method = RequestMethod.Get;
            var uri = new RawRequestUriBuilder();
            uri.Reset(_endpoint);
            uri.AppendPath("/subscriptions/", false);
            uri.AppendPath(subscriptionId, true);
            uri.AppendPath("/resourceGroups/", false);
            uri.AppendPath(resourceGroupName, true);
            uri.AppendPath("/providers/Microsoft.DataFactory/factories/", false);
            uri.AppendPath(factoryName, true);
            uri.AppendPath("/managedVirtualNetworks/", false);
            uri.AppendPath(managedVirtualNetworkName, true);
            uri.AppendPath("/managedPrivateEndpoints", false);
            uri.AppendQuery("api-version", _apiVersion, true);
            request.Uri = uri;
            request.Headers.Add("Accept", "application/json");
            _userAgent.Apply(message);
            return message;
        }

        /// <summary> Lists managed private endpoints. </summary>
        /// <param name="subscriptionId"> The subscription identifier. </param>
        /// <param name="resourceGroupName"> The resource group name. </param>
        /// <param name="factoryName"> The factory name. </param>
        /// <param name="managedVirtualNetworkName"> Managed virtual network name. </param>
        /// <param name="cancellationToken"> The cancellation token to use. </param>
        /// <exception cref="ArgumentNullException"> <paramref name="subscriptionId"/>, <paramref name="resourceGroupName"/>, <paramref name="factoryName"/> or <paramref name="managedVirtualNetworkName"/> is null. </exception>
        /// <exception cref="ArgumentException"> <paramref name="subscriptionId"/>, <paramref name="resourceGroupName"/>, <paramref name="factoryName"/> or <paramref name="managedVirtualNetworkName"/> is an empty string, and was expected to be non-empty. </exception>
        public async Task<Response<DataFactoryPrivateEndpointListResult>> ListByFactoryAsync(string subscriptionId, string resourceGroupName, string factoryName, string managedVirtualNetworkName, CancellationToken cancellationToken = default)
        {
            Argument.AssertNotNullOrEmpty(subscriptionId, nameof(subscriptionId));
            Argument.AssertNotNullOrEmpty(resourceGroupName, nameof(resourceGroupName));
            Argument.AssertNotNullOrEmpty(factoryName, nameof(factoryName));
            Argument.AssertNotNullOrEmpty(managedVirtualNetworkName, nameof(managedVirtualNetworkName));

            using var message = CreateListByFactoryRequest(subscriptionId, resourceGroupName, factoryName, managedVirtualNetworkName);
            await _pipeline.SendAsync(message, cancellationToken).ConfigureAwait(false);
            switch (message.Response.Status)
            {
                case 200:
                    {
                        DataFactoryPrivateEndpointListResult value = default;
                        using var document = await JsonDocument.ParseAsync(message.Response.ContentStream, default, cancellationToken).ConfigureAwait(false);
                        value = DataFactoryPrivateEndpointListResult.DeserializeDataFactoryPrivateEndpointListResult(document.RootElement);
                        return Response.FromValue(value, message.Response);
                    }
                default:
                    throw new RequestFailedException(message.Response);
            }
        }

        /// <summary> Lists managed private endpoints. </summary>
        /// <param name="subscriptionId"> The subscription identifier. </param>
        /// <param name="resourceGroupName"> The resource group name. </param>
        /// <param name="factoryName"> The factory name. </param>
        /// <param name="managedVirtualNetworkName"> Managed virtual network name. </param>
        /// <param name="cancellationToken"> The cancellation token to use. </param>
        /// <exception cref="ArgumentNullException"> <paramref name="subscriptionId"/>, <paramref name="resourceGroupName"/>, <paramref name="factoryName"/> or <paramref name="managedVirtualNetworkName"/> is null. </exception>
        /// <exception cref="ArgumentException"> <paramref name="subscriptionId"/>, <paramref name="resourceGroupName"/>, <paramref name="factoryName"/> or <paramref name="managedVirtualNetworkName"/> is an empty string, and was expected to be non-empty. </exception>
        public Response<DataFactoryPrivateEndpointListResult> ListByFactory(string subscriptionId, string resourceGroupName, string factoryName, string managedVirtualNetworkName, CancellationToken cancellationToken = default)
        {
            Argument.AssertNotNullOrEmpty(subscriptionId, nameof(subscriptionId));
            Argument.AssertNotNullOrEmpty(resourceGroupName, nameof(resourceGroupName));
            Argument.AssertNotNullOrEmpty(factoryName, nameof(factoryName));
            Argument.AssertNotNullOrEmpty(managedVirtualNetworkName, nameof(managedVirtualNetworkName));

            using var message = CreateListByFactoryRequest(subscriptionId, resourceGroupName, factoryName, managedVirtualNetworkName);
            _pipeline.Send(message, cancellationToken);
            switch (message.Response.Status)
            {
                case 200:
                    {
                        DataFactoryPrivateEndpointListResult value = default;
                        using var document = JsonDocument.Parse(message.Response.ContentStream);
                        value = DataFactoryPrivateEndpointListResult.DeserializeDataFactoryPrivateEndpointListResult(document.RootElement);
                        return Response.FromValue(value, message.Response);
                    }
                default:
                    throw new RequestFailedException(message.Response);
            }
        }

        internal HttpMessage CreateCreateOrUpdateRequest(string subscriptionId, string resourceGroupName, string factoryName, string managedVirtualNetworkName, string managedPrivateEndpointName, DataFactoryPrivateEndpointData data, string ifMatch)
        {
            var message = _pipeline.CreateMessage();
            var request = message.Request;
            request.Method = RequestMethod.Put;
            var uri = new RawRequestUriBuilder();
            uri.Reset(_endpoint);
            uri.AppendPath("/subscriptions/", false);
            uri.AppendPath(subscriptionId, true);
            uri.AppendPath("/resourceGroups/", false);
            uri.AppendPath(resourceGroupName, true);
            uri.AppendPath("/providers/Microsoft.DataFactory/factories/", false);
            uri.AppendPath(factoryName, true);
            uri.AppendPath("/managedVirtualNetworks/", false);
            uri.AppendPath(managedVirtualNetworkName, true);
            uri.AppendPath("/managedPrivateEndpoints/", false);
            uri.AppendPath(managedPrivateEndpointName, true);
            uri.AppendQuery("api-version", _apiVersion, true);
            request.Uri = uri;
            if (ifMatch != null)
            {
                request.Headers.Add("If-Match", ifMatch);
            }
            request.Headers.Add("Accept", "application/json");
            request.Headers.Add("Content-Type", "application/json");
            var content = new Utf8JsonRequestContent();
            content.JsonWriter.WriteObjectValue(data);
            request.Content = content;
            _userAgent.Apply(message);
            return message;
        }

        /// <summary> Creates or updates a managed private endpoint. </summary>
        /// <param name="subscriptionId"> The subscription identifier. </param>
        /// <param name="resourceGroupName"> The resource group name. </param>
        /// <param name="factoryName"> The factory name. </param>
        /// <param name="managedVirtualNetworkName"> Managed virtual network name. </param>
        /// <param name="managedPrivateEndpointName"> Managed private endpoint name. </param>
        /// <param name="data"> Managed private endpoint resource definition. </param>
        /// <param name="ifMatch"> ETag of the managed private endpoint entity. Should only be specified for update, for which it should match existing entity or can be * for unconditional update. </param>
        /// <param name="cancellationToken"> The cancellation token to use. </param>
        /// <exception cref="ArgumentNullException"> <paramref name="subscriptionId"/>, <paramref name="resourceGroupName"/>, <paramref name="factoryName"/>, <paramref name="managedVirtualNetworkName"/>, <paramref name="managedPrivateEndpointName"/> or <paramref name="data"/> is null. </exception>
        /// <exception cref="ArgumentException"> <paramref name="subscriptionId"/>, <paramref name="resourceGroupName"/>, <paramref name="factoryName"/>, <paramref name="managedVirtualNetworkName"/> or <paramref name="managedPrivateEndpointName"/> is an empty string, and was expected to be non-empty. </exception>
        public async Task<Response<DataFactoryPrivateEndpointData>> CreateOrUpdateAsync(string subscriptionId, string resourceGroupName, string factoryName, string managedVirtualNetworkName, string managedPrivateEndpointName, DataFactoryPrivateEndpointData data, string ifMatch = null, CancellationToken cancellationToken = default)
        {
            Argument.AssertNotNullOrEmpty(subscriptionId, nameof(subscriptionId));
            Argument.AssertNotNullOrEmpty(resourceGroupName, nameof(resourceGroupName));
            Argument.AssertNotNullOrEmpty(factoryName, nameof(factoryName));
            Argument.AssertNotNullOrEmpty(managedVirtualNetworkName, nameof(managedVirtualNetworkName));
            Argument.AssertNotNullOrEmpty(managedPrivateEndpointName, nameof(managedPrivateEndpointName));
            Argument.AssertNotNull(data, nameof(data));

            using var message = CreateCreateOrUpdateRequest(subscriptionId, resourceGroupName, factoryName, managedVirtualNetworkName, managedPrivateEndpointName, data, ifMatch);
            await _pipeline.SendAsync(message, cancellationToken).ConfigureAwait(false);
            switch (message.Response.Status)
            {
                case 200:
                    {
                        DataFactoryPrivateEndpointData value = default;
                        using var document = await JsonDocument.ParseAsync(message.Response.ContentStream, default, cancellationToken).ConfigureAwait(false);
                        value = DataFactoryPrivateEndpointData.DeserializeDataFactoryPrivateEndpointData(document.RootElement);
                        return Response.FromValue(value, message.Response);
                    }
                default:
                    throw new RequestFailedException(message.Response);
            }
        }

        /// <summary> Creates or updates a managed private endpoint. </summary>
        /// <param name="subscriptionId"> The subscription identifier. </param>
        /// <param name="resourceGroupName"> The resource group name. </param>
        /// <param name="factoryName"> The factory name. </param>
        /// <param name="managedVirtualNetworkName"> Managed virtual network name. </param>
        /// <param name="managedPrivateEndpointName"> Managed private endpoint name. </param>
        /// <param name="data"> Managed private endpoint resource definition. </param>
        /// <param name="ifMatch"> ETag of the managed private endpoint entity. Should only be specified for update, for which it should match existing entity or can be * for unconditional update. </param>
        /// <param name="cancellationToken"> The cancellation token to use. </param>
        /// <exception cref="ArgumentNullException"> <paramref name="subscriptionId"/>, <paramref name="resourceGroupName"/>, <paramref name="factoryName"/>, <paramref name="managedVirtualNetworkName"/>, <paramref name="managedPrivateEndpointName"/> or <paramref name="data"/> is null. </exception>
        /// <exception cref="ArgumentException"> <paramref name="subscriptionId"/>, <paramref name="resourceGroupName"/>, <paramref name="factoryName"/>, <paramref name="managedVirtualNetworkName"/> or <paramref name="managedPrivateEndpointName"/> is an empty string, and was expected to be non-empty. </exception>
        public Response<DataFactoryPrivateEndpointData> CreateOrUpdate(string subscriptionId, string resourceGroupName, string factoryName, string managedVirtualNetworkName, string managedPrivateEndpointName, DataFactoryPrivateEndpointData data, string ifMatch = null, CancellationToken cancellationToken = default)
        {
            Argument.AssertNotNullOrEmpty(subscriptionId, nameof(subscriptionId));
            Argument.AssertNotNullOrEmpty(resourceGroupName, nameof(resourceGroupName));
            Argument.AssertNotNullOrEmpty(factoryName, nameof(factoryName));
            Argument.AssertNotNullOrEmpty(managedVirtualNetworkName, nameof(managedVirtualNetworkName));
            Argument.AssertNotNullOrEmpty(managedPrivateEndpointName, nameof(managedPrivateEndpointName));
            Argument.AssertNotNull(data, nameof(data));

            using var message = CreateCreateOrUpdateRequest(subscriptionId, resourceGroupName, factoryName, managedVirtualNetworkName, managedPrivateEndpointName, data, ifMatch);
            _pipeline.Send(message, cancellationToken);
            switch (message.Response.Status)
            {
                case 200:
                    {
                        DataFactoryPrivateEndpointData value = default;
                        using var document = JsonDocument.Parse(message.Response.ContentStream);
                        value = DataFactoryPrivateEndpointData.DeserializeDataFactoryPrivateEndpointData(document.RootElement);
                        return Response.FromValue(value, message.Response);
                    }
                default:
                    throw new RequestFailedException(message.Response);
            }
        }

        internal HttpMessage CreateGetRequest(string subscriptionId, string resourceGroupName, string factoryName, string managedVirtualNetworkName, string managedPrivateEndpointName, string ifNoneMatch)
        {
            var message = _pipeline.CreateMessage();
            var request = message.Request;
            request.Method = RequestMethod.Get;
            var uri = new RawRequestUriBuilder();
            uri.Reset(_endpoint);
            uri.AppendPath("/subscriptions/", false);
            uri.AppendPath(subscriptionId, true);
            uri.AppendPath("/resourceGroups/", false);
            uri.AppendPath(resourceGroupName, true);
            uri.AppendPath("/providers/Microsoft.DataFactory/factories/", false);
            uri.AppendPath(factoryName, true);
            uri.AppendPath("/managedVirtualNetworks/", false);
            uri.AppendPath(managedVirtualNetworkName, true);
            uri.AppendPath("/managedPrivateEndpoints/", false);
            uri.AppendPath(managedPrivateEndpointName, true);
            uri.AppendQuery("api-version", _apiVersion, true);
            request.Uri = uri;
            if (ifNoneMatch != null)
            {
                request.Headers.Add("If-None-Match", ifNoneMatch);
            }
            request.Headers.Add("Accept", "application/json");
            _userAgent.Apply(message);
            return message;
        }

        /// <summary> Gets a managed private endpoint. </summary>
        /// <param name="subscriptionId"> The subscription identifier. </param>
        /// <param name="resourceGroupName"> The resource group name. </param>
        /// <param name="factoryName"> The factory name. </param>
        /// <param name="managedVirtualNetworkName"> Managed virtual network name. </param>
        /// <param name="managedPrivateEndpointName"> Managed private endpoint name. </param>
        /// <param name="ifNoneMatch"> ETag of the managed private endpoint entity. Should only be specified for get. If the ETag matches the existing entity tag, or if * was provided, then no content will be returned. </param>
        /// <param name="cancellationToken"> The cancellation token to use. </param>
        /// <exception cref="ArgumentNullException"> <paramref name="subscriptionId"/>, <paramref name="resourceGroupName"/>, <paramref name="factoryName"/>, <paramref name="managedVirtualNetworkName"/> or <paramref name="managedPrivateEndpointName"/> is null. </exception>
        /// <exception cref="ArgumentException"> <paramref name="subscriptionId"/>, <paramref name="resourceGroupName"/>, <paramref name="factoryName"/>, <paramref name="managedVirtualNetworkName"/> or <paramref name="managedPrivateEndpointName"/> is an empty string, and was expected to be non-empty. </exception>
        public async Task<Response<DataFactoryPrivateEndpointData>> GetAsync(string subscriptionId, string resourceGroupName, string factoryName, string managedVirtualNetworkName, string managedPrivateEndpointName, string ifNoneMatch = null, CancellationToken cancellationToken = default)
        {
            Argument.AssertNotNullOrEmpty(subscriptionId, nameof(subscriptionId));
            Argument.AssertNotNullOrEmpty(resourceGroupName, nameof(resourceGroupName));
            Argument.AssertNotNullOrEmpty(factoryName, nameof(factoryName));
            Argument.AssertNotNullOrEmpty(managedVirtualNetworkName, nameof(managedVirtualNetworkName));
            Argument.AssertNotNullOrEmpty(managedPrivateEndpointName, nameof(managedPrivateEndpointName));

            using var message = CreateGetRequest(subscriptionId, resourceGroupName, factoryName, managedVirtualNetworkName, managedPrivateEndpointName, ifNoneMatch);
            await _pipeline.SendAsync(message, cancellationToken).ConfigureAwait(false);
            switch (message.Response.Status)
            {
                case 200:
                    {
                        DataFactoryPrivateEndpointData value = default;
                        using var document = await JsonDocument.ParseAsync(message.Response.ContentStream, default, cancellationToken).ConfigureAwait(false);
                        value = DataFactoryPrivateEndpointData.DeserializeDataFactoryPrivateEndpointData(document.RootElement);
                        return Response.FromValue(value, message.Response);
                    }
                case 404:
                    return Response.FromValue((DataFactoryPrivateEndpointData)null, message.Response);
                default:
                    throw new RequestFailedException(message.Response);
            }
        }

        /// <summary> Gets a managed private endpoint. </summary>
        /// <param name="subscriptionId"> The subscription identifier. </param>
        /// <param name="resourceGroupName"> The resource group name. </param>
        /// <param name="factoryName"> The factory name. </param>
        /// <param name="managedVirtualNetworkName"> Managed virtual network name. </param>
        /// <param name="managedPrivateEndpointName"> Managed private endpoint name. </param>
        /// <param name="ifNoneMatch"> ETag of the managed private endpoint entity. Should only be specified for get. If the ETag matches the existing entity tag, or if * was provided, then no content will be returned. </param>
        /// <param name="cancellationToken"> The cancellation token to use. </param>
        /// <exception cref="ArgumentNullException"> <paramref name="subscriptionId"/>, <paramref name="resourceGroupName"/>, <paramref name="factoryName"/>, <paramref name="managedVirtualNetworkName"/> or <paramref name="managedPrivateEndpointName"/> is null. </exception>
        /// <exception cref="ArgumentException"> <paramref name="subscriptionId"/>, <paramref name="resourceGroupName"/>, <paramref name="factoryName"/>, <paramref name="managedVirtualNetworkName"/> or <paramref name="managedPrivateEndpointName"/> is an empty string, and was expected to be non-empty. </exception>
        public Response<DataFactoryPrivateEndpointData> Get(string subscriptionId, string resourceGroupName, string factoryName, string managedVirtualNetworkName, string managedPrivateEndpointName, string ifNoneMatch = null, CancellationToken cancellationToken = default)
        {
            Argument.AssertNotNullOrEmpty(subscriptionId, nameof(subscriptionId));
            Argument.AssertNotNullOrEmpty(resourceGroupName, nameof(resourceGroupName));
            Argument.AssertNotNullOrEmpty(factoryName, nameof(factoryName));
            Argument.AssertNotNullOrEmpty(managedVirtualNetworkName, nameof(managedVirtualNetworkName));
            Argument.AssertNotNullOrEmpty(managedPrivateEndpointName, nameof(managedPrivateEndpointName));

            using var message = CreateGetRequest(subscriptionId, resourceGroupName, factoryName, managedVirtualNetworkName, managedPrivateEndpointName, ifNoneMatch);
            _pipeline.Send(message, cancellationToken);
            switch (message.Response.Status)
            {
                case 200:
                    {
                        DataFactoryPrivateEndpointData value = default;
                        using var document = JsonDocument.Parse(message.Response.ContentStream);
                        value = DataFactoryPrivateEndpointData.DeserializeDataFactoryPrivateEndpointData(document.RootElement);
                        return Response.FromValue(value, message.Response);
                    }
                case 404:
                    return Response.FromValue((DataFactoryPrivateEndpointData)null, message.Response);
                default:
                    throw new RequestFailedException(message.Response);
            }
        }

        internal HttpMessage CreateDeleteRequest(string subscriptionId, string resourceGroupName, string factoryName, string managedVirtualNetworkName, string managedPrivateEndpointName)
        {
            var message = _pipeline.CreateMessage();
            var request = message.Request;
            request.Method = RequestMethod.Delete;
            var uri = new RawRequestUriBuilder();
            uri.Reset(_endpoint);
            uri.AppendPath("/subscriptions/", false);
            uri.AppendPath(subscriptionId, true);
            uri.AppendPath("/resourceGroups/", false);
            uri.AppendPath(resourceGroupName, true);
            uri.AppendPath("/providers/Microsoft.DataFactory/factories/", false);
            uri.AppendPath(factoryName, true);
            uri.AppendPath("/managedVirtualNetworks/", false);
            uri.AppendPath(managedVirtualNetworkName, true);
            uri.AppendPath("/managedPrivateEndpoints/", false);
            uri.AppendPath(managedPrivateEndpointName, true);
            uri.AppendQuery("api-version", _apiVersion, true);
            request.Uri = uri;
            request.Headers.Add("Accept", "application/json");
            _userAgent.Apply(message);
            return message;
        }

        /// <summary> Deletes a managed private endpoint. </summary>
        /// <param name="subscriptionId"> The subscription identifier. </param>
        /// <param name="resourceGroupName"> The resource group name. </param>
        /// <param name="factoryName"> The factory name. </param>
        /// <param name="managedVirtualNetworkName"> Managed virtual network name. </param>
        /// <param name="managedPrivateEndpointName"> Managed private endpoint name. </param>
        /// <param name="cancellationToken"> The cancellation token to use. </param>
        /// <exception cref="ArgumentNullException"> <paramref name="subscriptionId"/>, <paramref name="resourceGroupName"/>, <paramref name="factoryName"/>, <paramref name="managedVirtualNetworkName"/> or <paramref name="managedPrivateEndpointName"/> is null. </exception>
        /// <exception cref="ArgumentException"> <paramref name="subscriptionId"/>, <paramref name="resourceGroupName"/>, <paramref name="factoryName"/>, <paramref name="managedVirtualNetworkName"/> or <paramref name="managedPrivateEndpointName"/> is an empty string, and was expected to be non-empty. </exception>
        public async Task<Response> DeleteAsync(string subscriptionId, string resourceGroupName, string factoryName, string managedVirtualNetworkName, string managedPrivateEndpointName, CancellationToken cancellationToken = default)
        {
            Argument.AssertNotNullOrEmpty(subscriptionId, nameof(subscriptionId));
            Argument.AssertNotNullOrEmpty(resourceGroupName, nameof(resourceGroupName));
            Argument.AssertNotNullOrEmpty(factoryName, nameof(factoryName));
            Argument.AssertNotNullOrEmpty(managedVirtualNetworkName, nameof(managedVirtualNetworkName));
            Argument.AssertNotNullOrEmpty(managedPrivateEndpointName, nameof(managedPrivateEndpointName));

            using var message = CreateDeleteRequest(subscriptionId, resourceGroupName, factoryName, managedVirtualNetworkName, managedPrivateEndpointName);
            await _pipeline.SendAsync(message, cancellationToken).ConfigureAwait(false);
            switch (message.Response.Status)
            {
                case 200:
                case 204:
                    return message.Response;
                default:
                    throw new RequestFailedException(message.Response);
            }
        }

        /// <summary> Deletes a managed private endpoint. </summary>
        /// <param name="subscriptionId"> The subscription identifier. </param>
        /// <param name="resourceGroupName"> The resource group name. </param>
        /// <param name="factoryName"> The factory name. </param>
        /// <param name="managedVirtualNetworkName"> Managed virtual network name. </param>
        /// <param name="managedPrivateEndpointName"> Managed private endpoint name. </param>
        /// <param name="cancellationToken"> The cancellation token to use. </param>
        /// <exception cref="ArgumentNullException"> <paramref name="subscriptionId"/>, <paramref name="resourceGroupName"/>, <paramref name="factoryName"/>, <paramref name="managedVirtualNetworkName"/> or <paramref name="managedPrivateEndpointName"/> is null. </exception>
        /// <exception cref="ArgumentException"> <paramref name="subscriptionId"/>, <paramref name="resourceGroupName"/>, <paramref name="factoryName"/>, <paramref name="managedVirtualNetworkName"/> or <paramref name="managedPrivateEndpointName"/> is an empty string, and was expected to be non-empty. </exception>
        public Response Delete(string subscriptionId, string resourceGroupName, string factoryName, string managedVirtualNetworkName, string managedPrivateEndpointName, CancellationToken cancellationToken = default)
        {
            Argument.AssertNotNullOrEmpty(subscriptionId, nameof(subscriptionId));
            Argument.AssertNotNullOrEmpty(resourceGroupName, nameof(resourceGroupName));
            Argument.AssertNotNullOrEmpty(factoryName, nameof(factoryName));
            Argument.AssertNotNullOrEmpty(managedVirtualNetworkName, nameof(managedVirtualNetworkName));
            Argument.AssertNotNullOrEmpty(managedPrivateEndpointName, nameof(managedPrivateEndpointName));

            using var message = CreateDeleteRequest(subscriptionId, resourceGroupName, factoryName, managedVirtualNetworkName, managedPrivateEndpointName);
            _pipeline.Send(message, cancellationToken);
            switch (message.Response.Status)
            {
                case 200:
                case 204:
                    return message.Response;
                default:
                    throw new RequestFailedException(message.Response);
            }
        }

        internal HttpMessage CreateListByFactoryNextPageRequest(string nextLink, string subscriptionId, string resourceGroupName, string factoryName, string managedVirtualNetworkName)
        {
            var message = _pipeline.CreateMessage();
            var request = message.Request;
            request.Method = RequestMethod.Get;
            var uri = new RawRequestUriBuilder();
            uri.Reset(_endpoint);
            uri.AppendRawNextLink(nextLink, false);
            request.Uri = uri;
            request.Headers.Add("Accept", "application/json");
            _userAgent.Apply(message);
            return message;
        }

        /// <summary> Lists managed private endpoints. </summary>
        /// <param name="nextLink"> The URL to the next page of results. </param>
        /// <param name="subscriptionId"> The subscription identifier. </param>
        /// <param name="resourceGroupName"> The resource group name. </param>
        /// <param name="factoryName"> The factory name. </param>
        /// <param name="managedVirtualNetworkName"> Managed virtual network name. </param>
        /// <param name="cancellationToken"> The cancellation token to use. </param>
        /// <exception cref="ArgumentNullException"> <paramref name="nextLink"/>, <paramref name="subscriptionId"/>, <paramref name="resourceGroupName"/>, <paramref name="factoryName"/> or <paramref name="managedVirtualNetworkName"/> is null. </exception>
        /// <exception cref="ArgumentException"> <paramref name="subscriptionId"/>, <paramref name="resourceGroupName"/>, <paramref name="factoryName"/> or <paramref name="managedVirtualNetworkName"/> is an empty string, and was expected to be non-empty. </exception>
        public async Task<Response<DataFactoryPrivateEndpointListResult>> ListByFactoryNextPageAsync(string nextLink, string subscriptionId, string resourceGroupName, string factoryName, string managedVirtualNetworkName, CancellationToken cancellationToken = default)
        {
            Argument.AssertNotNull(nextLink, nameof(nextLink));
            Argument.AssertNotNullOrEmpty(subscriptionId, nameof(subscriptionId));
            Argument.AssertNotNullOrEmpty(resourceGroupName, nameof(resourceGroupName));
            Argument.AssertNotNullOrEmpty(factoryName, nameof(factoryName));
            Argument.AssertNotNullOrEmpty(managedVirtualNetworkName, nameof(managedVirtualNetworkName));

            using var message = CreateListByFactoryNextPageRequest(nextLink, subscriptionId, resourceGroupName, factoryName, managedVirtualNetworkName);
            await _pipeline.SendAsync(message, cancellationToken).ConfigureAwait(false);
            switch (message.Response.Status)
            {
                case 200:
                    {
                        DataFactoryPrivateEndpointListResult value = default;
                        using var document = await JsonDocument.ParseAsync(message.Response.ContentStream, default, cancellationToken).ConfigureAwait(false);
                        value = DataFactoryPrivateEndpointListResult.DeserializeDataFactoryPrivateEndpointListResult(document.RootElement);
                        return Response.FromValue(value, message.Response);
                    }
                default:
                    throw new RequestFailedException(message.Response);
            }
        }

        /// <summary> Lists managed private endpoints. </summary>
        /// <param name="nextLink"> The URL to the next page of results. </param>
        /// <param name="subscriptionId"> The subscription identifier. </param>
        /// <param name="resourceGroupName"> The resource group name. </param>
        /// <param name="factoryName"> The factory name. </param>
        /// <param name="managedVirtualNetworkName"> Managed virtual network name. </param>
        /// <param name="cancellationToken"> The cancellation token to use. </param>
        /// <exception cref="ArgumentNullException"> <paramref name="nextLink"/>, <paramref name="subscriptionId"/>, <paramref name="resourceGroupName"/>, <paramref name="factoryName"/> or <paramref name="managedVirtualNetworkName"/> is null. </exception>
        /// <exception cref="ArgumentException"> <paramref name="subscriptionId"/>, <paramref name="resourceGroupName"/>, <paramref name="factoryName"/> or <paramref name="managedVirtualNetworkName"/> is an empty string, and was expected to be non-empty. </exception>
        public Response<DataFactoryPrivateEndpointListResult> ListByFactoryNextPage(string nextLink, string subscriptionId, string resourceGroupName, string factoryName, string managedVirtualNetworkName, CancellationToken cancellationToken = default)
        {
            Argument.AssertNotNull(nextLink, nameof(nextLink));
            Argument.AssertNotNullOrEmpty(subscriptionId, nameof(subscriptionId));
            Argument.AssertNotNullOrEmpty(resourceGroupName, nameof(resourceGroupName));
            Argument.AssertNotNullOrEmpty(factoryName, nameof(factoryName));
            Argument.AssertNotNullOrEmpty(managedVirtualNetworkName, nameof(managedVirtualNetworkName));

            using var message = CreateListByFactoryNextPageRequest(nextLink, subscriptionId, resourceGroupName, factoryName, managedVirtualNetworkName);
            _pipeline.Send(message, cancellationToken);
            switch (message.Response.Status)
            {
                case 200:
                    {
                        DataFactoryPrivateEndpointListResult value = default;
                        using var document = JsonDocument.Parse(message.Response.ContentStream);
                        value = DataFactoryPrivateEndpointListResult.DeserializeDataFactoryPrivateEndpointListResult(document.RootElement);
                        return Response.FromValue(value, message.Response);
                    }
                default:
                    throw new RequestFailedException(message.Response);
            }
        }
    }
}